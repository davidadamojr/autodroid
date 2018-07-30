# Android settings
ADB_PATH = "/home/davidadamojr/Android/Sdk/platform-tools/adb"

# Autodroid settings
OUTPUT_PATH = "/home/davidadamojr/git/autodroid/output"
AUTODROID_PATH = "/home/davidadamojr/git/autodroid"
EVENT_INTERVAL = 2
TEST_SETUP = "Standard"
EVENT_SELECTION_STRATEGY = "gaussian_random"
TERMINATION_CRITERION = "Length"
COMPLETION_CRITERION = "Length"
TEST_TEARDOWN = "Standard"
TEST_SUITE_LENGTH = 20  # only used if completion criterion is "Length"
TIME_BUDGET = 1  # (in hours) only used if completion criterion is "Time"
TERMINATION_PROBABILITY = 0.05  # only used when termination criterion is "probabilistic"
TEST_CASE_LENGTH = 20  # only used if termination criterion is "length"
STRINGS_PATH = "strings.txt"
COVERAGE_BROADCAST = "com.davidadamojr.tester.finishtesting"

# AUT settings
APK_PATH = "/home/davidadamojr/git/autodroid/apps/oi_shoppinglist_2_1_3.apk"
APP_PACKAGE_NAME = "org.openintents.shopping"
COVERAGE_FILE_PATH = "/mnt/sdcard/org.openintents.shopping"

# Device settings
DEVICE_ID = "emulator-"