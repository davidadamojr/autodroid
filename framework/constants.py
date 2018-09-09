import os
from config import TOOL_PATH


class Script:
    CLEAR_DATA = os.path.join(TOOL_PATH, "scripts", "clear_data.sh")
    CLEAR_LOGS = os.path.join(TOOL_PATH, "scripts", "clear_logs.sh")
    GET_PROCESS_ID = os.path.join(TOOL_PATH, "scripts", "get_process_id.sh")
    GET_COVERAGE = os.path.join(TOOL_PATH, "scripts", "retrieve_coverage.sh")
    GET_LOGS = os.path.join(TOOL_PATH, "scripts", "retrieve_logs.sh")

