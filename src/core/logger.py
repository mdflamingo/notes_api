import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.config import settings

LOG_FORMAT = '{"asctime": "%(asctime)s", "levelname": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'

LOG_DEFAULT_HANDLERS = ['console', ]
logs_dir = Path(settings.logs_dir)
logs_dir.mkdir(exist_ok=True)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        request = getattr(record, 'request', None)
        if request:
            record.request_id = request.headers.get('X-Request-Id')
        return True


def setup_root_logger():

    logger = logging.getLogger('root')
    formatter = logging.Formatter(LOG_FORMAT)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    file = RotatingFileHandler(filename=settings.logs_file_name,
                               mode=settings.logs_mode,
                               maxBytes=settings.logs_max_bytes,
                               backupCount=settings.logs_backup_count)
    file.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file)
    logger.addFilter(RequestIdFilter())
    logger.setLevel(logging.INFO)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': LOG_FORMAT},
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {'handlers': LOG_DEFAULT_HANDLERS, 'level': 'INFO'},
        'uvicorn.error': {'level': 'INFO'},
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
