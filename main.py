import config
import initialization
import sys
import sqlite3
import database
import time
from subprocess import CalledProcessError
from generation import SuiteBuilder, MonkeyBuilder
from appiumatic.emulator import *
from appiumatic.exceptions import AdbNotFound, InvalidParameter

__author__ = "David Adamo Jr."

logger = logging.getLogger(__name__)

# reset adb
try:
    reset_adb(config.SDK_PATH)
except AdbNotFound as anf:
    logger.critical(anf)
    sys.exit(1)
except CalledProcessError:
    logger.critical("Failed to reset ADB. Please check your SDK path.")
    print("Failed to reset ADB. Please check your SDK path.")
    sys.exit(1)


def start_emulator():
    if config.USE_GENYMOTION:
        start_genymotion(config.SDK_PATH, config.GENYMOTION_PATH, config.VM_NAME, config.EMULATOR_BOOT_DELAY, tries=10)
    else:
        start_avd(config.SDK_PATH, config.AVD_NAME, config.EMULATOR_BOOT_DELAY, tries=10)


def stop_emulator():
    if config.USE_GENYMOTION:
        kill_genymotion()
    else:
        kill_avd(config.SDK_PATH)


def start_appium():
    logger.info("Starting appium...")
    subprocess.Popen("./scripts/start_appium.sh", shell=True)

    time.sleep(config.APPIUM_BOOT_DELAY) # wait for appium to start


def stop_appium():
    logger.info("Terminating appium process...")
    subprocess.call("./scripts/stop_appium.sh", shell=True)

def create_directories():
    os.make

    return test_suite_dir, test_case_dir, logs_dir, coverage_dir

# initialize framework parameters
try:
    event_selection_strategy = initialization.event_selection_strategy(config.EVENT_SELECTION_STRATEGY,
                                                                       config.EVENT_COMBINATION_STRENGTH)
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

start_emulator()
start_appium()

db_connection = sqlite3.connect("db/autodroid.db")
database.create_tables(db_connection)

if config.MONKEY_MODE:
    if config.COMPLETION_CRITERION.lower() == "events":
        monkey_builder = MonkeyBuilder(config.APK_PATH, config.EVENT_INTERVAL, db_connection)
        monkey_builder.generate_monkey_test(config.APK_PATH, event_selection_strategy, completion_criterion, setup,
                                            teardown)
    else:
        print("Monkey mode can only be used with the 'events' completion criterion.")
        logger.debug("Invalid completion criterion for monkey mode.")
else:
    current_time = int(time.time())

    suite_builder = SuiteBuilder(config.APK_PATH, config.EVENT_INTERVAL, test_suite_dir, db_connection)
    suite_builder.generate_test_suite(event_selection_strategy, termination_criterion, completion_criterion, setup,
                                      teardown)

db_connection.close()
stop_appium()
stop_emulator()



