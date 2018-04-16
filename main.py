import sqlite3
import logging
import sys
import config
from framework import database
from framework import generation
from framework import initialization
from appiumatic.exceptions import InvalidParameter

logger = logging.getLogger(__name__)


def retrieve_text_values(strings_path):
    with open(strings_path) as strings_file:
        text_field_strings = strings_file.readlines()

    return text_field_strings


def main():
    try:
        event_selection_strategy = initialization.event_selection_strategy(config.EVENT_SELECTION_STRATEGY)
        termination_criterion = initialization.termination_criterion(config.TERMINATION_CRITERION,
                                                                     config.TERMINATION_PROBABILITY,
                                                                     config.TEST_CASE_LENGTH)
        completion_criterion = initialization.completion_criterion(config.COMPLETION_CRITERION,
                                                                   config.TIME_BUDGET,
                                                                   config.TEST_SUITE_LENGTH)
        setup = initialization.setup_strategy(config.TEST_SETUP)
        teardown = initialization.tear_down_strategy(config.TEST_TEARDOWN)
    except InvalidParameter as ip:
        logger.critical(ip)
        sys.exit(1)

    db_connection = sqlite3.connect("db/autodroid.db")
    logger.debug("Connection to database successful.")

    database.create_tables(db_connection)
    logger.debug("Table creation successful.")

    try:
        text_values = retrieve_text_values(config.STRINGS_PATH)
        configuration = {
            "apk_path": config.APK_PATH,
            "apk_package_name": config.APP_PACKAGE_NAME,
            "coverage_path": config.COVERAGE_FILE_PATH,
            "event_interval": config.EVENT_INTERVAL,
            "text_entry_values": text_values
        }
        generation.construct_test_suite(db_connection, configuration, setup, event_selection_strategy,
                                        termination_criterion, completion_criterion, teardown)
    except IOError as file_read_failed:
        logger.fatal("Could not read strings file: {}".format(file_read_failed))
    except ConnectionRefusedError as conn_refused:
        logger.fatal("Could not connect to appium server: {}.".format(conn_refused))

    db_connection.close()

main()
