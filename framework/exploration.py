import logging
import time
import os
from selenium.common.exceptions import WebDriverException
from appiumatic.hashing import generate_sequence_hash
from framework.utils import adb

logger = logging.getLogger(__name__)


def get_logs(path_to_logs, sequence_count, app_process_id, adb_info):
    log_file_name = "log{}.txt".format(str(sequence_count).zfill(3))
    log_file_path = os.path.join(path_to_logs, log_file_name)
    adb.get_logs(adb_path=adb_info.path,
                 log_file_path=log_file_path,
                 process_id=app_process_id,
                 device_id=adb_info.device_id)


def get_coverage(path_to_coverage, sequence_count, device_coverage_path,  adb_info):
    coverage_file_path = os.path.join(device_coverage_path, "coverage.ec")
    coverage_file_name = "coverage{}.ec".format(str(sequence_count).zfill(3))
    adb.get_coverage(adb_path=adb_info.path,
                     device_path=coverage_file_path,
                     coverage_path=path_to_coverage,
                     coverage_name=coverage_file_name,
                     broadcast=adb_info.coverage_broadcast,
                     device_id=adb_info.device_id)


class Explorer:
    def __init__(self, database, sequence_generator, completion_criterion, adb_info, app_info):
        self.database = database
        self.sequence_generator = sequence_generator
        self.completion_criterion = completion_criterion
        self.adb_info = adb_info
        self.app_info = app_info

    def explore(self, suite_info, output_paths):
        suite_duration = 0
        sequence_count = 0
        while not self.completion_criterion(suite_duration=suite_duration, sequence_count=sequence_count):
            logger.debug("Path to APK is {}".format(self.app_info.apk_path))
            try:
                sequence_info = self.sequence_generator.initialize()
                app_process_id = adb.get_process_id(adb_path=self.adb_info.path,
                                                    package_name=self.app_info.package_name,
                                                    device_id=self.adb_info.device_id)
                sequence_duration = self.sequence_generator.generate(sequence_info,
                                                                     self.app_info.package_name,
                                                                     suite_info.id)
            except WebDriverException as e:
                print(e)
                continue  # start a new test case

            get_logs(output_paths.logs, sequence_count + 1, app_process_id, self.adb_info)
            get_coverage(output_paths.coverage, sequence_count + 1, self.app_info.coverage_file_path, self.adb_info)

            self.sequence_generator.finalize(sequence_count=sequence_count + 1,
                                             suite_id=suite_info.id,
                                             sequence_info=sequence_info,
                                             output_paths=output_paths)

            sequence_count += 1
            suite_duration += sequence_duration
            logger.debug("Suite has been running for {} seconds.".format(suite_duration))

        self.finalize_exploration(suite_info)

    def finalize_exploration(self, suite_info):
        suite_end_time = int(time.time())
        suite_duration = suite_end_time - suite_info.creation_time
        self.database.update_suite(suite_info.id, suite_end_time, suite_duration)
        print("Test suite generation took {} seconds.".format(suite_duration))
