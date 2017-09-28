# Android settings
SDK_PATH = "/home/davidadamojr/Android/Sdk"
EMULATOR_BOOT_DELAY = 5

# Standard emulator settings
AVD_NAME = "api19_0"

# Genymotion settings
USE_GENYMOTION = True
GENYMOTION_PATH = "/home/davidadamojr/genymotion"
VM_NAME = "3942e954-84c4-4766-8e4b-6901dfeebde8"

# Autodroid settings
USE_MENU_KEY = False
MONKEY_MODE = False
EVENT_INTERVAL = 2
INITIAL_CONTEXT_STRATEGY = None
TEST_SETUP = "Standard"
EVENT_SELECTION_STRATEGY = "Random"
TERMINATION_CRITERION = "Probabilistic"
COMPLETION_CRITERION = "Time"
TEST_TEARDOWN = "Standard"
TEST_SUITE_LENGTH = 100 # only used if completion criterion is "Length"
TIME_BUDGET = 60 # only used if completion criterion is "Time"
EVENT_COUNT = 1000 # only used for monkey testing (i.e. MONKEY_MODE=True), and if completion criterion is "Events"
EVENT_COMBINATION_STRENGTH = 2 # only used when event selection strategy is "nway"
TERMINATION_PROBABILITY = 0.05 # only used when termination criterion is "probabilistic"
TEST_CASE_LENGTH = 100 # only used if termination criterion is "length"

# Appium settings
APPIUM_START_CMD = "appium"
APPIUM_BOOT_DELAY = 15

# AUT settings
APK_PATH = "apps/org.tomdroid-0.7.5.apk"
APP_PACKAGE_NAME = "org.tomdroid"
COVERAGE_FILE_PATH = "/mnt/sdcard/org.tomdroid"
