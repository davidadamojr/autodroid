import logging
from appiumatic.emulator import start_avd
logger = logging.getLogger(__name__)
logger.info("Starting from import script!")
start_avd("/home/davidadamojr/Android/Sdk", "api19_0")

