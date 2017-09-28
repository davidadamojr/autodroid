import logging
import logging.config
import os
import json

if os.path.isfile("appiumatic.log"):
    os.remove("appiumatic.log")

if os.path.isfile("autodroid.log"):
    os.remove("autodroid.log")

with open("logging.json") as logging_configuration_file:
    config = json.load(logging_configuration_file)

logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
logger.info("Appiumatic logger configuration complete!")