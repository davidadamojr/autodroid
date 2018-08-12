import logging
import sqlite3
import config
import framework.initialization as initialization
from functools import partial
from collections import namedtuple
from framework.database import Database
from framework.exploration import Explorer
from appiumatic.exploration.sequence import SequenceGenerator
from appiumatic.execution import Executor
from appiumatic.paths import create_output_directories

logger = logging.getLogger(__name__)


def create_database():
    db_connection = sqlite3.connect("db/autodroid.db")
    logger.debug("Connection to database successful.")
    database = Database(db_connection)
    database.create_tables()
    return database


def create_explorer(database, text_values):
    sequence_generator = create_sequence_generator(database, text_values)
    completion_criterion = initialization.completion_criterion(config.COMPLETION_CRITERION,
                                                               config.TIME_BUDGET,
                                                               config.TEST_SUITE_LENGTH)
    AppInfo = namedtuple("AppInfo", ["apk_path", "package_name", "coverage_file_path"])
    app_info = AppInfo(config.APK_PATH, config.APP_PACKAGE_NAME, config.COVERAGE_FILE_PATH)

    AdbInfo = namedtuple("AdbInfo", ["path", "device_id", "coverage_broadcast"])
    adb_info = AdbInfo(config.ADB_PATH, config.DEVICE_ID, config.COVERAGE_BROADCAST)

    return Explorer(database, sequence_generator, completion_criterion, adb_info, app_info)


def create_sequence_generator(database, text_values):
    termination_criterion = initialization.termination_criterion(config.TERMINATION_CRITERION,
                                                                 config.TERMINATION_PROBABILITY,
                                                                 config.TEST_CASE_LENGTH)
    event_selection_strategy = initialization.event_selection_strategy(config.EVENT_SELECTION_STRATEGY)
    setup_strategy = initialization.setup_strategy(config.TEST_SETUP,
                                                   config.APK_PATH,
                                                   config.ADB_PATH,
                                                   config.DEVICE_ID)
    tear_down_strategy = initialization.tear_down_strategy(config.TEST_TEARDOWN, config.ADB_PATH, config.DEVICE_ID)
    executor_factory = partial(create_executor,
                               event_interval=config.EVENT_INTERVAL,
                               text_values=text_values)
    sequence_generator = SequenceGenerator(database,
                                           termination_criterion,
                                           event_selection_strategy,
                                           setup_strategy,
                                           tear_down_strategy,
                                           executor_factory)
    return sequence_generator


def create_executor(driver, event_interval, text_values):
    return Executor(driver, event_interval, text_values)


def retrieve_text_values():
    with open(config.STRINGS_PATH) as strings_file:
        text_field_strings = strings_file.readlines()
        text_field_strings = [text.replace("\n", "") for text in text_field_strings]

    return text_field_strings


def create_directories(suite_creation_time):
    return create_output_directories(config.APP_PACKAGE_NAME, config.OUTPUT_PATH, suite_creation_time)

