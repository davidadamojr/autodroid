import xml.etree.ElementTree as etree
from abstractions import create_partial_events, create_state, create_action

__author__ = "David Adamo Jr."

CLICK = "click"
LONG_CLICK = "long-click"
CHECK_UNCHECK = "*check"
SCROLL_UP_DOWN = "scroll*"

def get_available_events(driver):
    page_source = driver.page_source



def get_possible_actions(page_source):
    possible_actions = []
    actionable_widgets = _get_actionable_widgets(page_source)
    for action_type, widgets in actionable_widgets.items():
        for widget in widgets:
            actions = extract_actions(action_type, widget)


def extract_actions(action_type, widget):
    widget_actions = []
    if action_type == CLICK:
        widget_action = create_action("click", widget)
    elif action_type == LONG_CLICK:
        widget_action = create_action("long-click", widget)
    elif action_type == CHECK_UNCHECK:



def _get_actionable_widgets(page_source):
    """*check represents check/uncheck, scroll* represents scrollup/scrolldown"""
    actionable_widgets = {
        CLICK: [],
        LONG_CLICK: [],
        CHECK: []
        UNCHECK: [],
        SCROLL_UP: []
        SCROLL_DOWN: []
    }

    xml_element = etree.fromstring(page_source)
    xml_tree = etree.ElementTree(xml_element)

    # depth first traversal of elements
    element_stack = [xml_tree.getroot()]
    while element_stack:
        current_element = element_stack.pop()
        element_attributes = current_element.attrib
        if element_attributes.get("clickable", "false") == "true":
            actionable_widgets["click"].append(current_element)
        if element_attributes.get("long-clickable", "false") == "true":
            actionable_widgets["long-click"].append(current_element)
        if element_attributes.get("checkable", "false") == "true":
            actionable_widgets["check"].append(current_element)
        if element_attributes.get("scrollable", "false") == "true":
            actionable_widgets["scroll*"].append(current_element)
        element_stack.extend(list(current_element))

    return actionable_widgets


def get_current_state(driver):
    page_source = driver.page_source
    possible_actions = get_possible_actions(page_source)
    current_activity = driver.current_activity

