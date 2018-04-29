import logging
import subprocess
from framework.constants import *

logger = logging.getLogger(__name__)


def clear_sdcard_data(adb_path):
    clear_sdcard_cmd = "{} {}".format(Script.CLEAR_DATA, adb_path)
    subprocess.check_call(clear_sdcard_cmd, shell=True)
    logger.info("Successfully cleared SD card data.")


def clear_logs(adb_path):
    clear_logs_cmd = "{} {}".format(Script.CLEAR_LOGS, adb_path)
    subprocess.check_call(clear_logs_cmd, shell=True)
    logger.info("Successfully cleared logs.")


def get_process_id(adb_path, package_name):
    process_id_cmd = "{} {} {}".format(Script.GET_PROCESS_ID, adb_path, package_name)
    process = subprocess.Popen(process_id_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = subprocess.communicate()
