import logging
import os
from paste.translogger import TransLogger


def sesam_logger(logger_name, timestamp=False, app=None):
    if logger_name is None or logger_name is '':
        raise ValueError('Please provide the valid logger name.')
    logger = logging.getLogger(logger_name)
    log_level = os.getenv('LOG_LEVEL')
    level = logging.getLevelName(log_level.upper()) if log_level is not None else None
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                                                  if timestamp else '%(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(stdout_handler)
    if not isinstance(level, int):
        logger.warning("Unsupported value or no LOG_LEVEL provided. Hence, setting default log level to INFO.")
        level = logging.INFO
    logger.setLevel(level)

    if app:
        wsgi_log_format_string = ('"%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" '
                                  '%(status)s %(bytes)s')

        app.wsgi_app = TransLogger(app.wsgi_app, logger_name=logger.name, format=wsgi_log_format_string,
                                   setup_console_handler=False, set_logger_level=logger.level)

    return logger



