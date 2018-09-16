# Autodroid - Automatic Exploration of GUI-based Android Applications

Only works on Linux systems.

## Dependencies
- lxml - https://lxml.de/
- Appium - https://github.com/appium/python-client
- Python 3.5 - https://www.python.org/downloads/release/python-355/

## Setup Instructions

1. Clone the repository as follows: "git clone --recursive https://github.com/davidadamojr/autodroid.git"
2. Install Appium 1.7.0. Run the `install_appium.sh` script in the `scripts` folder.
3. Make sure you have pip installed for Python 3. Install virtualenv with the following command: `pip3 install virtualenv`.
4. In the `autodroid` root directory, create a virtual environment with name `venv` with the following command: `virtualenv venv`

## Configuration and Usage Instructions

The `config.py` file contains configuration parameters that determine which exploration and sequence generation strategies Autodroid will use
during an exploration session. Please set the appropriate parameters as necessary. Each configuration parameter is explained below:

- *ADB_PATH:* Absolute path to your Android Debug Bridge (ADB) installation (e.g. `/home/user/Android/Sdk/platform-tools/adb`).
- *OUTPUT_PATH:* Absolute path that indicates where Combodroid should save event sequences, log files and coverage files (e.g. `home/user/git/combodroid/output`).
- *AUTODROID_PATH:* Absolute path to your Combdroid installation.
- *EVENT_INTERVAL:* Time between execution of events during automatic exploration (in seconds).
- *TEST_SETUP:* Test setup strategy. The default and only strategy is `standard`.
- *EVENT_SELECTION_STRATEGY:* Event selection strategy to use during automatic exploration. Chose one of `random` or `combinatorial`.
- *TERMINATION_CRITERION:* The criterion used to terminate each exploration sequence. An exploration sequence is a sequence of events. Choose one of `length` or `probabilistic`. The `length` criterion ends an exploration sequence after a specified number of events.
- *COMPLETION_CRITERION:* The criterion used to terminate a set of exploration sequences (test suite). Default and only setting is `length` which ends a testing session after a specified number of exploration sequences.
- *TEST_TEARDOWN:* Test teardown strategy. Default and only strategy is `standard`.
- *TEST_SUITE_LENGTH:*:  Specifies the number of exploration sequences in a single test session. This setting only applies when the `COMPLETION_CRITERION` is `length`.
- *TIME_BUDGET:* Future capability.
- *TERMINATION_PROBABILITY:* The probability of ending an exploration sequence. This value ranges from 0 to 1 and only applies when the `TERMINATION_CRITERION` is set to `probabilistic`.
- *TEST_CASE_LENGTH:* The maximum number of events in each exploration sequence. This number can range from 0 to infinity. This setting only applies when the `TERMINATION_CRITERION` is set to `length`.
- *STRINGS_PATH:* Path to text file that contains a list of strings to use when Combodroid encounters text input fields during automatic exploration.
- *COVERAGE_BROADCAST:* Intent broadcast to collect code coverage files from emulator or device.
- *APK_PATH:* Absolute path to Application Under Test (AUT) (e.g. `home/user/git/combodroid/apps/org.tomdroid-0.7.5.apk`)
- *APP_PACKAGE_NAME:* Package name of AUT (e.g. `org.tomdroid`)
- *COVERAGE_FILE_PATH:* Path to store coverage files on the device or emulator (e.g `/mnt/sdcard/org.tomdroid`)

Execute the `run.sh` script in the combodroid root directory to begin automatic exploration using the settings in the `config.py` file. The script takes one argument that represents the number of exploration suites to generate.
```
./run.sh 10
```
The command above will perform 10 different exploration sessions.
