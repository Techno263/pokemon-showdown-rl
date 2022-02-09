'''
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(room_id)s : %(msg_type)s - %(message)s',
)

_loggers = {}

def get_logger(username, room_id=None):
    if room_id == None:
        logger_name = username
    else:
        logger_name = f'{username}.{room_id}'
    if logger_name in _loggers:
        return _loggers[logger_name]
    else:
        logger = logging.getLogger(logger_name)
        fh = logging.FileHandler(f'logs/{logger_name}.log')
        logger.addHandler(fh)
        _loggers[logger_name] = logger
        return logger
'''
