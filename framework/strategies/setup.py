from appium import webdriver
from framework.utils.scripts import clear_sdcard_data


def standard(apk_path, adb_path):
    clear_sdcard_data(adb_path)
    driver = _get_driver(apk_path)
    return driver


def _get_driver(apk_path):
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",
        "app": apk_path,
        "newCommandTimeout": 3600,
        "autoGrantPermissions": True,
        "fullReset": True
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    return driver
