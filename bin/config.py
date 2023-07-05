# Imports
import traceback
import binascii
import logging
import os

### Environmental Variables ###
# LOG_LEVEL = INFO
# LOG_PATH = /logs
# LOG_RETENTION_DAYS = 5
# PROJECTOR_BRAND = benq
# PROJECTOR_PORT = /dev/ttyUSB0
# PROJECTOR_COOLDOWN_MINUTES = 10
# API_TOKEN = <AUTO_GENERATED>

# Attributes
PROJECTOR_BRANDS = ['benq']
LOG_LEVEL = 'INFO'
LOG_PATH = '/logs'
LOG_RETENTION_DAYS = 5
PROJECTOR_BRAND = 'benq'
PROJECTOR_PORT = '/dev/ttyUSB0'
PROJECTOR_COOLDOWN_MINUTES = 10
API_TOKEN = binascii.hexlify(os.urandom(16)).decode()

# Class
class Config:
    def __init__(self, path):
        self.data = None
        
        try:
            # Validate LOG_LEVEL
            LOG_LEVEL = os.environ['LOG_LEVEL'] if os.environ['LOG_LEVEL'] else LOG_LEVEL
            logging.getLevelName(LOG_LEVEL)
            # Validate LOG_PATH
            LOG_PATH = os.environ['LOG_PATH'] if os.environ['LOG_PATH'] else LOG_PATH
            if not os.path.exists(LOG_PATH):
                raise Exception('{} log path does not exist! Please create one.'.format(LOG_PATH))
            # Validate LOG_RETENTION_DAYS
            LOG_RETENTION_DAYS = os.environ['LOG_RETENTION_DAYS'] if os.environ['LOG_RETENTION_DAYS'] else LOG_RETENTION_DAYS
            if LOG_RETENTION_DAYS.isnumeric():
                if not int(LOG_RETENTION_DAYS) >= 1:
                    raise Exception('Invalid LOG_RETENTION_DAYS number! It must be greater then or equal to 1.')
            else:
                raise Exception('Invalid LOG_RETENTION_DAYS value! It must be numeric and greater than or equal to 1.')

            # Validate PROJECTOR_BRAND
            PROJECTOR_BRAND = os.environ['PROJECTOR_BRAND'] if os.environ['PROJECTOR_BRAND'] else PROJECTOR_BRAND
            if not PROJECTOR_BRAND in PROJECTOR_BRANDS:
                raise Exception('This controller only works with the following brand(s): {}'.format(','.join(PROJECTOR_BRANDS)))
            # Validate PROJECTOR_PORT
            PROJECTOR_PORT = os.environ['PROJECTOR_PORT'] if os.environ['PROJECTOR_PORT'] else PROJECTOR_PORT
            if not os.path.isfile(PROJECTOR_PORT):
                raise Exception('Unable to find or access this serial port: {}'.format(PROJECTOR_PORT))
            # Validate PROJECTOR_COOLDOWN_MINUTES
            PROJECTOR_COOLDOWN_MINUTES = os.environ['PROJECTOR_COOLDOWN_MINUTES'] if os.environ['PROJECTOR_COOLDOWN_MINUTES'] else PROJECTOR_COOLDOWN_MINUTES
            if PROJECTOR_COOLDOWN_MINUTES.isnumeric():
                if int(PROJECTOR_COOLDOWN_MINUTES) < 1:
                    raise Exception('Invalid PROJECTOR_COOLDOWN_MINUTES number! It must be greater then or equal to 1.')
            else:
                raise Exception('Invalid PROJECTOR_COOLDOWN_MINUTES value! It must be numeric and greater than or equal to 1.')
            # Validate API_TOKEN
            API_TOKEN = os.environ['API_TOKEN'] if os.environ['API_TOKEN'] else API_TOKEN
            if len(API_TOKEN) < 16:
                raise Exception('Invalid API_TOKEN value! It must be 16 characters or longer to ensure it\'s secure!')
            if not os.environ['API_TOKEN']:
                print('INFO: Here\'s the auto-generated API_TOKEN for use: {}'.format(API_TOKEN))
                print('INFO: Please make sure to use API_TOKEN environment variable to keep the token consistent at every restart.')

        except Exception as ex:
            print('ERROR: Unable to load config file! Reason: {}\nStacktrace Error:\n{}'.format(str(ex), traceback.format_exc()))
