import sqlite3
import time
import logging
import sys
import config
from framework import database
from framework import generation
from framework import initialization
from appiumatic.exceptions import InvalidParameter

logger = logging.getLogger(__name__)

try:
    event_selection_strategy = initialization.event_selection_strategy(config.EVENT_SELECTION_STRATEGY)
    termination_criterion = initialization.termination_criterion(config.TERMINATION_CRITERION,
                                                                 config.TERMINATION_PROBABILITY,
                                                                 config.TEST_CASE_LENGTH)
    completion_criterion = initialization.completion_criterion(config.COMPLETION_CRITERION,
                                                               config.EVENT_COUNT,
                                                               config.TIME_BUDGET,
                                                               config.TEST_SUITE_LENGTH)
    setup = initialization.setup(config.TEST_SETUP)
    teardown = initialization.teardown(config.TEST_TEARDOWN)
except InvalidParameter as ip:
    logger.critical(ip)
    sys.exit(1)

db_connection = sqlite3.connect("db/autodroid.db")
database.create_tables(db_connection)

try:
    aut_info = {"apk_path": config.APK_PATH, "apk_package_name": config.APP_PACKAGE_NAME,
                "coverage_path": config.COVERAGE_FILE_PATH}
    generation.construct_test_suite(db_connection, aut_info, setup, event_selection_strategy, termination_criterion,
                                    completion_criterion, teardown)
except ConnectionRefusedError as conn_refused:
    logger.fatal("Could not connect to appium server: %s.".format(conn_refused))

db_connection.close()