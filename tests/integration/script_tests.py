import unittest
import config
from framework.utils.scripts import *


"""These tests require a running emulator"""
class ScriptTests(unittest.TestCase):

    def test_clear_sdcard_data(self):
        clear_sdcard_data(config.ADB_PATH)

    def test_clear_logs(self):
        clear_logs(config.ADB_PATH)