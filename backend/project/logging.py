import os
from project.settings import BASE_DIR

LOGS_DIR = os.path.join(BASE_DIR, 'logs')
if os.environ.get('LOGS_DIR', None):
    LOGS_DIR = os.environ.get('LOGS_DIR')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s %(process)d]: %(message)s',
        },
    },
    'handlers': {
        'update_currencies_history': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'update_currencies_history.log'),
            'formatter': 'standard',
        },
        'fill_up_currencies': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'fill_up_currencies.log'),
            'formatter': 'standard',
        },
    },
    'loggers': {
        'update_currencies_history': {
            'handlers': ['update_currencies_history'],
            'level': 'INFO',
            'propagate': True,
        },
        'fill_up_currencies': {
            'handlers': ['fill_up_currencies'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}