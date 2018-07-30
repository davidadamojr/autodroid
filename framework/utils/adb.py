import logging
import subprocess
from framework.constants import *

logger = logging.getLogger(__name__)


def clear_sdcard_data(adb_path, device_id):
    clear_sdcard_cmd = "{} {} {}".format(Script.CLEAR_DATA, adb_path, device_id)
    subprocess.check_call(clear_sdcard_cmd, shell=True)
    logger.info("Successfully cleared SD card data.")


def clear_logs(adb_path, device_id):
    clear_logs_cmd = "{} {} {}".format(Script.CLEAR_LOGS, adb_path, device_id)
    subprocess.check_call(clear_logs_cmd, shell=True)
    logger.info("Successfully cleared logs.")


def get_process_id(adb_path, package_name, device_id):
    process_id_cmd = "{} {} {} {}".format(Script.GET_PROCESS_ID, adb_path, package_name, device_id)
    process = subprocess.Popen(process_id_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = process.communicate()
    process_id = output.decode("utf-8").strip()
    logger.info("Process id for {} is {}.".format(package_name, adb_path))
    return process_id


def get_coverage(adb_path, device_path, coverage_path, coverage_name, broadcast, device_id):
    get_coverage_cmd = "{} {} {} {} {} {} {}".format(Script.GET_COVERAGE, adb_path, device_path, coverage_path,
                                                     coverage_name, broadcast, device_id)
    subprocess.call(get_coverage_cmd, shell=True)
    logger.info("Successfully retrieved coverage file: {}.".format(coverage_name))


def get_logs(adb_path, log_file_path, process_id, device_id):
    get_logs_cmd = "{} {} {} {} {}".format(Script.GET_LOGS, adb_path, log_file_path, process_id, device_id)
    subprocess.call(get_logs_cmd, shell=True)
    logger.info("Successfully retrieved log file: {}".format(log_file_path))
