# Imports
import traceback
import logging
import yaml
import os

### Environmental Variables ###
# CONFIG_PATH = /config
# LOG_LEVEL = INFO
# LOG_PATH = /logs
# LOG_RETENTION_DAYS = 5
# PROJECTOR_BRAND = benq
# PROJECTOR_PORT = /dev/ttyUSB0
# PROJECTOR_COOLDOWN_MINUTES = 10

# Attributes
PROJECTOR_BRANDS = ['benq']

# Class
class Config:
    def __init__(self, path):
        self.data = None
        
        CONFIG_PATH = os.environ['CONFIG_PATH'] if os.environ['CONFIG_PATH'] else '/config/config.yml'
        with open(CONFIG_PATH) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        
        try:
            # Validate log.level
            LOG_LEVEL = os.environ['LOG_LEVEL'] if os.environ['LOG_LEVEL'] else self.config['log']['level']
            logging.getLevelName(LOG_LEVEL)
            # Validate log.path
            LOG_PATH = os.environ['LOG_PATH'] if os.environ['LOG_PATH'] else self.config['log']['level']
            if not os.path.exists(LOG_PATH):
                raise Exception('{} log path does not exist! Please create one.'.format(LOG_PATH))
            # Validate log.retention_days
            LOG_RETENTION_DAYS = os.environ['LOG_RETENTION_DAYS'] if os.environ['LOG_RETENTION_DAYS'] else self.config['log']['retention_days']
            if LOG_RETENTION_DAYS.isnumeric():
                if not int(LOG_RETENTION_DAYS) >= 1:
                    raise Exception('Invalid retention_days number! It must be greater then or equal to 1.')
            else:
                raise Exception('Invalid retention_days value! It must be numeric and greater than or equal to 1.')

            # Validate projector.brand
            PROJECTOR_BRAND = os.environ['PROJECTOR_BRAND'] if os.environ['PROJECTOR_BRAND'] else self.config['projector']['brand']
            if not PROJECTOR_BRAND in PROJECTOR_BRANDS:
                raise Exception('This controller only works with the following brand(s): {}'.format(','.join(PROJECTOR_BRANDS)))
            # Validate projector.port
            PROJECTOR_PORT = os.environ['PROJECTOR_PORT'] if os.environ['PROJECTOR_PORT'] else self.config['projector']['port']
            if not os.path.isfile(PROJECTOR_PORT):
                raise Exception('Unable to find or access this serial port: {}'.format(PROJECTOR_PORT))
            # Validate projector.cooldown_minutes
            PROJECTOR_COOLDOWN_MINUTES = os.environ['PROJECTOR_COOLDOWN_MINUTES'] if os.environ['PROJECTOR_COOLDOWN_MINUTES'] else self.config['projector']['cooldown_minutes']
            if PROJECTOR_COOLDOWN_MINUTES.isnumeric():
                if not int(PROJECTOR_COOLDOWN_MINUTES) >= 1:
                    raise Exception('Invalid cooldown_minutes number! It must be greater then or equal to 1.')
            else:
                raise Exception('Invalid cooldown_minutes value! It must be numeric and greater than or equal to 1.')

        except Exception as ex:
            print('ERROR: Unable to load config file! Reason: {}\nStacktrace Error:\n{}'.format(str(ex), traceback.format_exc()))
