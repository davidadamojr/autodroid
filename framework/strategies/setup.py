from appium import webdriver
from framework.utils.adb import clear_sdcard_data


def standard(apk_path, adb_path, device_id):
    clear_sdcard_data(adb_path, device_id)
    driver = _get_driver(apk_path, device_id)
    return driver

from appium import webdriver
from framework.utils.adb import clear_sdcard_data, change_context
import random
import logging
logger = logging.getLogger(__name__)

def standard(apk_path, adb_path, device_id, context_sequence=None):
    clear_sdcard_data(adb_path, device_id)
    driver = _get_driver(apk_path, device_id)
    return driver

def random_start(apk_path, adb_path, device_id, context_sequence):
    clear_sdcard_data(adb_path, device_id)
    selected_row = random.choice(context_sequence.context_covering_array)
    if selected_row[0] == "CHANGE_LANDSCAPE":
        ch_orientation = 1
    elif selected_row[0] == "CHANGE_PORTRAIT":
        ch_orientation = 0
    if selected_row[1] == "POWER_ON":
        ch_power = 1
    elif selected_row[1] == "POWER_OFF":
        ch_power = 0
    if selected_row[2] == "INTERNET_CONNECTED":
        ch_internet = 1
    elif selected_row[2] == "INTERNET_DISCONNECTED":
        ch_internet = 0
    if selected_row[3] == "BATTERY_LOW":
        ch_battery = 0
    elif selected_row[3] == "BATTERY_OK":
        ch_battery = 1
    elif selected_row[3] == "BATTERY_HIGH":
        ch_battery = 2
    change_context(adb_path, ch_orientation, ch_power, ch_internet, ch_battery)
    driver = _get_driver(apk_path, device_id)
    return driver

def iterative_start(apk_path, adb_path, device_id, context_sequence):
    clear_sdcard_data(adb_path, device_id)
    selected_row = context_sequence.context_covering_array[context_sequence.covering_array_index]
    if selected_row[0] == "CHANGE_LANDSCAPE":
        ch_orientation = 1
    elif selected_row[0] == "CHANGE_PORTRAIT":
        ch_orientation = 0
    if selected_row[1] == "POWER_ON":
        ch_power = 1
    elif selected_row[1] == "POWER_OFF":
        ch_power = 0
    if selected_row[2] == "INTERNET_CONNECTED":
        ch_internet = 1
    elif selected_row[2] == "INTERNET_DISCONNECTED":
        ch_internet = 0
    if selected_row[3] == "BATTERY_LOW":
        ch_battery = 0
    elif selected_row[3] == "BATTERY_OK":
        ch_battery = 1
    elif selected_row[3] == "BATTERY_HIGH":
        ch_battery = 2
    change_context(adb_path, ch_orientation, ch_power, ch_internet, ch_battery)
    driver = _get_driver(apk_path, device_id)
    context_sequence.covering_array_index = context_sequence.iterate_covering_array(context_sequence.covering_array_index)
    return driver


def _get_driver(apk_path, device_id):
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",
        "app": apk_path,
        "newCommandTimeout": 3600,
        "autoGrantPermissions": True,
        "fullReset": True,
        "disableWindowAnimation": True,
        "appWaitActivity": "*",
        "udid": device_id
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    return driver


def _get_driver(apk_path, device_id):
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",
        "app": apk_path,
        "newCommandTimeout": 3600,
        "autoGrantPermissions": True,
        "fullReset": True,
        "disableWindowAnimation": True,
        "appWaitActivity": "*",
        "udid": device_id
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    return driver
