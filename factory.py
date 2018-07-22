import logging
import sqlite3
import config
import framework.initialization as initialization
from framework.database import Database
from appiumatic.generation import SuiteGenerator, SequenceGenerator

logger = logging.getLogger(__name__)


def create_database():
    db_connection = sqlite3.connect("db/autodroid.db")
    logger.debug("Connection to database successful.")
    database = Database(db_connection)
    database.create_tables()
    return database


def create_suite_generator(database):
    sequence_generator = create_sequence_generator(database)
    completion_criterion = initialization.completion_criterion(config.COMPLETION_CRITERION,
                                                               config.TIME_BUDGET,
                                                               config.TEST_SUITE_LENGTH)
    suite_generator = SuiteGenerator(database, sequence_generator, completion_criterion)
    return suite_generator


def create_sequence_generator(database):
    termination_criterion = initialization.termination_criterion(config.TERMINATION_CRITERION,
                                                                 config.TERMINATION_PROBABILITY,
                                                                 config.TEST_CASE_LENGTH)
    event_selection_strategy = initialization.event_selection_strategy(config.EVENT_SELECTION_STRATEGY)
    setup_strategy = initialization.setup_strategy(config.TEST_SETUP)
    tear_down_strategy = initialization.tear_down_strategy(config.TEST_TEARDOWN)
    sequence_generator = SequenceGenerator(database,
                                           termination_criterion,
                                           event_selection_strategy,
                                           setup_strategy,
                                           tear_down_strategy)
    return sequence_generator


def retrieve_text_values(strings_path):
    with open(strings_path) as strings_file:
        text_field_strings = strings_file.readlines()
        text_field_strings = [text.replace("\n", "") for text in text_field_strings]

    return text_field_strings

