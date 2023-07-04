# Imports
import bin.pyjector
import threading
import traceback
import datetime
import logging
import flask
import time
import bin
import os

# Attributes
app = flask.Flask(__name__)
config = None
log = None

# Functions
def load_config():
    global config
    config = bin.config.Config(os.env('PROJECTOR_CONFIG_PATH'))

def setup_logging():
    global log
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    log = logging.getLogger()
    fileHandler = logging.handlers.TimedRotatingFileHandler(os.path.join(config['log']['path'], 'activity.log'),
                                                            when="d",
                                                            interval=1,
                                                            backupCount=config['log']['retention_days'])
    fileHandler.setFormatter(logFormatter)
    log.addHandler(fileHandler)
    # consoleHandler = logging.StreamHandler(sys.stdout)
    # consoleHandler.setFormatter(logFormatter)
    # log.addHandler(consoleHandler)
    log.setLevel(logging.getLevelName(config['log']['level']))

# Classes
class Projector:
    def __init__(self):
        self.status = None
        self.lastOff = None
        self.device = bin.pyjector.Pyjector(port=config['projector']['port'], device_id=config['projector']['brand']) # https://github.com/JohnBrodie/pyjector
    
    def on(self):
        self.device.power('on')
        self.status = 'Online'
        log.info('Turned on the projector!')
    
    def off(self):
        self.device.power('off')
        self.status = 'Offline'
        self.lastOff = datetime.datetime.now()
        log.info('Turned off the projector!')

    def toggle(self, turnOn=None):
        if turnOn == None:
            if self.status == 'Offline':
                self.on()
            else:
                self.off()
        elif turnOn == True:
            self.on()
        else:
            self.off()
    
    def deviceStatus(self):
        status = self.device.power('status').strip()
        log.debug('Retrieved the status of the projector. Validating output...')
        if status.upper() == '*POW=OFF#':
            log.debug('Detected status of projector as offline!')
            return False
        elif status.upper() == '*POW=ON#':
            log.debug('Detected status of projector as online!')
            return True
        else:
            log.error('Unable to determine the status of the projector! Output received from the projector: {}'.format(status))
            raise Exception('Unable to determine the status of the projector! Output received from the projector: {}'.format(status))

    # Flask Functions
    @app.route('/status', methods=['GET'])
    def web_status(self):
        self.status = 'Offline'
        status = self.deviceStatus()
        if status:
            self.status = 'Online'
        return flask.jsonify({
            'status': status
        })

    @app.route('/toggle', methods=['POST'])
    def web_toggle(self):
        try:
            self.toggle()
            return flask.jsonify({
                'success': True
            })
        except Exception as ex:
            log.error('Unable to toggle projector. Reason: {}\nStacktrace Error:\n{}'.format(str(ex), traceback.format_exc()))
            return flask.jsonify({
                'success': False,
                'reason': str(ex)
            })

    @app.route('/on', methods=['POST'])
    def web_on(self):
        try:
            if self.lastOff and datetime.datetime.now() > (self.lastoff + datetime.timedelta(minutes=config['projector']['cooldown_minutes'])):
                print('INFO: It has not reached 10+ minutes since last shutdown. Please wait till after {} minutes before turning it back on.'.format(config['projector']['cooldown_minutes']))
                return flask.jsonify({
                    'success': False
                })

            self.on()
            return flask.jsonify({
                'success': True
            })
        except Exception as ex:
            log.error('Unable to turn on the projector. Reason: {}\nStacktrace Error:\n{}'.format(str(ex), traceback.format_exc()))
            return flask.jsonify({
                'success': False,
                'reason': str(ex)
            })

    @app.route('/off', methods=['POST'])
    def web_off(self):
        try:
            self.off()
            return flask.jsonify({
                'success': True
            })
        except Exception as ex:
            log.error('Unable to turn off the projector. Reason: {}\nStacktrace Error:\n{}'.format(str(ex), traceback.format_exc()))
            return flask.jsonify({
                'success': False,
                'reason': str(ex)
            })

# Threading
def projectorStatusThd():
    device = Projector()
    while True:
        device.deviceStatus()
        time.sleep(5)

# Main
def main():
    load_config()
    setup_logging()
    log.info('Starting projector status updater thread...')
    threading.Thread(target=projectorStatusThd, daemon=True, name='ProjectorThread')
    log.info('Listening for requests from HomeAssistant...')
    app.run(host='0.0.0.0', port=5000)

main()
