from appium import webdriver

__author__ = "David Adamo Jr."


def standard(apk_path):
    driver = _get_driver(apk_path)
    return driver


def _get_driver(apk_path):
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",
        "app": apk_path,
        "newCommandTimeout": 3600,
        "fullReset": True
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    return driver
