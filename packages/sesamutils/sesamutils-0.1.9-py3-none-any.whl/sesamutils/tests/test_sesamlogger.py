from sesamutils import sesam_logger

from pytest import raises
from testfixtures import LogCapture


def test_sesam_logger():
    with LogCapture() as expected_logger:
        actual_logger = sesam_logger('test_sesam_logger')
        actual_logger.setLevel(level='DEBUG')
        actual_logger.info('a info')
        actual_logger.error('an error')
        actual_name = actual_logger.name
        expected_logger.check(
            (actual_name, 'WARNING', 'Unsupported value or no LOG_LEVEL provided. '
                                     'Hence, setting default log level to INFO.'),
            (actual_name, 'INFO', 'a info'),
            (actual_name, 'ERROR', 'an error'),
        )


def test_logger_name_is_set():
    logger = sesam_logger('test_logger_name_is_set')
    assert logger.name == "test_logger_name_is_set"


def test_if_logger_name_is_blank():
    with raises(ValueError):
        logger = sesam_logger('')


def test_if_logger_name_is_none():
    with raises(ValueError):
        logger = sesam_logger(None)


def test_logger_without_timestamp():
    logger = sesam_logger('test_logger_without_timestamp', timestamp=False)
    assert logger.handlers[0].formatter._fmt == '%(name)s - %(levelname)s - %(message)s'


def test_logger_with_timestamp():
    logger = sesam_logger('test_logger_with_timestamp', timestamp=True)
    assert logger.handlers[0].formatter._fmt == '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
