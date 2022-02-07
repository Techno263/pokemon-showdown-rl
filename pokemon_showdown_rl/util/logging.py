
loggers = {}

def get_logger(logger_name):
    if logger_name in loggers:
        return loggers[logger_name]
    logger_fp = open(f'{logger_name}.log', 'at', encoding='utf8')
    loggers[logger_name] = logger_fp
    return logger_fp
