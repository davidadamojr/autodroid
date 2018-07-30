import logging
import config
import factory
from appiumatic.exceptions import InvalidParameter
from appiumatic.paths import create_output_directories

logger = logging.getLogger(__name__)


def main():
    database = factory.create_database()
    suite_info = database.create_suite()
    try:
        output_paths = create_output_directories(config.APP_PACKAGE_NAME,
                                                 config.OUTPUT_PATH,
                                                 suite_info.creation_time)
        text_values = factory.retrieve_text_values(config.STRINGS_PATH)
        explorer = factory.create_explorer(database, text_values)
        explorer.explore(suite_info, output_paths)
    except InvalidParameter as ip:
        logger.critical(ip)
    except IOError as io_error:
        logger.fatal(io_error)
    except ConnectionRefusedError as conn_refused:
        logger.fatal("Could not connect to appium server: {}.".format(conn_refused))

        # clean up - remove directories, remove database entries
    except Exception as e:
        logger.fatal("A fatal error occurred: {}".format(e))

        # clean up - remove directories, remove database entries

    database.close()


main()
