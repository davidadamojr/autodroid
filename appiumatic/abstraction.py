import logging

__author__ = "David Adamo Jr."

logger = logging.getLogger(__name__)

def create_target(selector, selectorValue, description, type, state):
    target = {
        "selector": selector,
        "selectorValue": selectorValue,
        "description": description,
        "type": type,
        "state": state
    }

    return target


def create_launch_event():
    target = create_target("system", "app", "launch", "launch", "enabled")
    action = create_action("launch", target)
    precondition = create_state(None, None)
    partial_event = create_partial_event(precondition, [action])

    return partial_event


def create_partial_event(precondition, actions):
    partial_event = {
        "precondition": precondition,
        "actions": actions
    }
    return partial_event


def create_partial_text_events(text_entry_actions, non_text_entry_actions):
    # events = []
    # if len(text_entry_actions) == 1:
    pass


def create_partial_events(current_state, possible_actions):
    events = []
    for action in possible_actions:
        event = create_partial_event(current_state, [action])
        events.append(event)

    return events


def create_back_event(precondition):
    target = create_target("key_code", "4", "back", "nav", "enabled")
    action = create_action("back", target)
    back_event = create_partial_event(precondition, [action])
    return back_event


def create_home_event(precondition):
    target = create_target("key_code", "3", "home", "nav", "enabled")
    action = create_action("home", target)
    home_event = create_partial_event(precondition, [action])
    return home_event


def create_action(action_type, widget):
    action = {
        "target": widget,
        "type": action_type,
        "value": None
    }
    return action


def create_ui_widget(xml_tree, element):
    selection_mechanism = _get_widget_selector(xml_tree, element)
    widget_description = _get_widget_description(element)
    widget_type = _get_widget_type(element)
    widget_state = _get_widget_state(element)
    target = {
        "selector": selection_mechanism[0],
        "selectorValue": selection_mechanism[1],
        "description": widget_description,
        "type": widget_type,
        "state": widget_state
    }

    return target


def _get_widget_state(element):
    element_attributes = element.attrib
    if element_attributes.get("enabled", "") == "true":
        return "enabled"

    return "disabled"


def _get_widget_type(element):
    element_attributes = element.attrib
    class_value = element_attributes.get("class", "")
    return class_value.split(".")[-1]


def _get_widget_selector(xml_tree, element):
    element_attributes = element.attrib
    resource_id = element_attributes.get("resource-id", "")
    id_not_unique = len(_get_elements_with_id(resource_id, xml_tree)) > 1
    if resource_id.strip() == "" or id_not_unique:
        return "xpath", xml_tree.getpath(element)

    return "id", resource_id


def _get_elements_with_id(resource_id, xml_tree):
    return xml_tree.getroot().findall(".//*[@resource-id='" + resource_id + "']".format(resource_id))


def _get_widget_description(element):
    element_attributes = element.attrib
    text_value = element_attributes.get("text", "").strip()
    content_desc_value = element_attributes.get("content-desc", "").strip()
    if text_value == "":
        if content_desc_value == "":
            description = ""
        else:
            description = content_desc_value
    else:
        description = text_value

    return description


def synthesize(partial_event, current_state):
    postcondition = {
        "activityName": current_state["activityName"],
        "stateId": current_state["stateId"]
    }
    partial_event["postcondition"] = postcondition
    return partial_event


def create_state(current_activity, state_id):
    state = {
        "activityName": current_activity,
        "stateId": state_id
    }

    return state


def create_crash_state():
    state= {
        "activityName": "crash",
        "stateId": "crash"
    }

    return state

