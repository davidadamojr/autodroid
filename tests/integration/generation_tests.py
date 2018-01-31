import os
import shutil
import unittest
import config

from framework import generation


def remove_output_files(output_path):
    if not os.path.exists(output_path):
        return

    output_file_names = os.listdir(output_path)
    for output_filename in output_file_names:
        file_path = os.path.join(output_path, output_filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.output_path = config.OUTPUT_PATH
        remove_output_files(self.output_path)

    def test_create_output_directories(self):
        # Arrange
        apk_package_name = "special_android_app"
        test_suite_creation_time = 1234567890

        # Act
        output_path = config.OUTPUT_PATH
        path_to_test_cases, path_to_logs, path_to_coverage = generation._create_output_directories(output_path,
                                                                                                   apk_package_name,
                                                                                                   test_suite_creation_time)

        # Assert
        self.assertEqual(path_to_test_cases, os.path.join(output_path, "{}_{}".format(apk_package_name, str(test_suite_creation_time)), "testcases"))
        self.assertEqual(path_to_logs, os.path.join(output_path, "{}_{}".format(apk_package_name, str(test_suite_creation_time)), "logs"))
        self.assertEqual(path_to_coverage, os.path.join(output_path, "{}_{}".format(apk_package_name, str(test_suite_creation_time)), "coverage"))
        self.assertEqual(os.path.exists(path_to_test_cases), True)
        self.assertEqual(os.path.exists(path_to_logs), True)
        self.assertEqual(os.path.exists(path_to_coverage), True)

    def tearDown(self):
        remove_output_files(self.output_path)