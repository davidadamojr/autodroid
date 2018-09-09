import unittest
import os
import config
from framework.utils import adb


"""These tests require a running emulator and the Tomdroid app"""

APP_PACKAGE = "org.tomdroid"


class ScriptTests(unittest.TestCase):

    def test_clear_sdcard_data(self):
        adb.clear_sdcard_data(config.ADB_PATH, config.DEVICE_ID)

    def test_clear_logs(self):
        adb.clear_logs(config.ADB_PATH, config.DEVICE_ID)

    def test_can_get_process_id(self):
        process_id = adb.get_process_id(config.ADB_PATH, APP_PACKAGE)
        print(process_id)

    def test_can_get_coverage(self):
        adb_path = config.ADB_PATH
        device_path = "/mnt/sdcard/" + APP_PACKAGE + "/coverage.ec"
        coverage_path = os.path.join(config.TOOL_PATH, "output")
        coverage_name = "coverage001.ec"
        broadcast = config.COVERAGE_BROADCAST
        device_id = config.DEVICE_ID

        adb.get_coverage(adb_path=adb_path,
                         device_path=device_path,
                         coverage_path=coverage_path,
                         coverage_name=coverage_name,
                         broadcast=broadcast,
                         device_id=device_id)

        self.assertIn(coverage_name, os.listdir(coverage_path))

        if os.path.isfile(os.path.join(coverage_path, coverage_name)):
            os.remove(os.path.join(coverage_path, coverage_name))

    def test_can_retrieve_logs(self):
        adb_path = config.ADB_PATH
        log_file_path = os.path.join(config.TOOL_PATH, "output", "log001.txt")
        device_id = config.DEVICE_ID
        process_id = adb.get_process_id(adb_path, APP_PACKAGE, device_id)

        adb.get_logs(adb_path=adb_path, log_file_path=log_file_path, process_id=process_id, device_id=device_id)

        self.assertIn("log001.txt", os.listdir(os.path.join(config.TOOL_PATH, "output")))

        if os.path.isfile(log_file_path):
            os.remove(log_file_path)



