# Android settings
ADB_PATH = "/home/davidadamojr/Android/Sdk/platform-tools/adb"

# Autodroid settings
OUTPUT_PATH = "/home/davidadamojr/git/autodroid/output"
TOOL_PATH = "/home/davidadamojr/git/autodroid"
EVENT_INTERVAL = 2
TEST_SETUP = "Standard"
EVENT_SELECTION_STRATEGY = "random"
TERMINATION_CRITERION = "Probabilistic"
COMPLETION_CRITERION = "Time"
TEST_TEARDOWN = "Standard"
TEST_SUITE_LENGTH = 10  # only used if completion criterion is "Length"
TIME_BUDGET = 900  # (in seconds) only used if completion criterion is "Time"
TERMINATION_PROBABILITY = 0.05  # only used when termination criterion is "probabilistic"
TEST_CASE_LENGTH = 20  # only used if termination criterion is "length"
STRINGS_PATH = "strings.txt"
COVERAGE_BROADCAST = "com.davidadamojr.tester.finishtesting"

# AUT settings
APK_PATH = "/home/davidadamojr/git/autodroid/apps/org.tomdroid-0.7.5.apk"
APP_PACKAGE_NAME = "org.tomdroid"
COVERAGE_FILE_PATH = "/mnt/sdcard/org.tomdroid"

# Device settings
DEVICE_ID = "emulator-5554"