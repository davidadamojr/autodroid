import logging
import config
import factory
from appiumatic.exceptions import InvalidParameter
from appiumatic.paths import create_output_directories

logger = logging.getLogger(__name__)


def main():
    database = factory.create_database()
    test_suite_info = database.create_test_suite()
    try:
        output_paths = create_output_directories(config.APP_PACKAGE_NAME,
                                                 config.OUTPUT_PATH,
                                                 test_suite_info.creation_time)
        text_values = factory.retrieve_text_values(config.STRINGS_PATH)
        suite_generator = factory.create_suite_generator(database)
        suite_generator.generate()
    except InvalidParameter as ip:
        logger.critical(ip)
    except IOError as io_error:
        logger.fatal(io_error)
    except ConnectionRefusedError as conn_refused:
        logger.fatal("Could not connect to appium server: {}.".format(conn_refused))
    except Exception as e:
        logger.fatal("A fatal error occurred: {}".format(e))

    database.close()


main()
