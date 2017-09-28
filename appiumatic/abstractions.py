__author__ = "David Adamo Jr."


CLICK = "click"
LONG_CLICK = "long-click"
CHECK_UNCHECK = "*check"
SCROLL_UP_DOWN = "scroll*"

def create_launch_event():
    target = {
        "selector": "system",
        "selectorValue": "app",
        "description": "launch",
        "type": "system",
    }
    action = {
        "target": target,
        "type": "launch",
        "value": None
    }
    precondition = {
        "activityName": None,
        "stateId": None
    }
    partial_event = {
        "actions": [action],
        "precondition": precondition
    }

    return partial_event

def create_action(action_type, widget):
    pass

def synthesize(partial_event, current_state):
    postcondition = {
        "activityName": current_state["activityName"],
        "stateId": current_state["stateId"]
    }
    partial_event["postcondition"] = postcondition
    return partial_event


def create_state(driver):
    pass


def create_partial_events():
    pass

