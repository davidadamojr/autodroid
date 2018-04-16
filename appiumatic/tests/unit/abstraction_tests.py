import abstraction
import constants
import unittest
import lxml.etree as etree


class AbstractionTests(unittest.TestCase):

    def test_create_launch_event(self):
        launch_event = abstraction.create_launch_event()
        expected_event = {
            "actions": [{
                "target": {
                    "selector": "system",
                    "selectorValue": "app",
                    "description": "launch",
                    "type": "launch",
                    "state": "enabled"
                },
                "type": "launch",
                "value": None
            }],
            "precondition": {
                "activityName": None,
                "stateId": None
            }
        }
        self.assertEqual(launch_event, expected_event)

    def test_create_action(self):
        action_type = constants.CLICK
        widget = {
            "selector": "id",
            "selectorValue": "widget_id",
            "description": "Login",
            "type": "Button",
            "state": "enabled"
        }
        created_action = abstraction.create_action(action_type, widget)
        expected_action = {
            "target": widget,
            "type": action_type,
            "value": None
        }
        self.assertEqual(created_action, expected_action)

    def test_create_ui_widget(self):
        document_xml = """<?xml version="1.0" encoding="UTF-8"?>
                        <hierarchy rotation="0"><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                        <nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/></nest>
                        <android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/></hierarchy>"""
        element = etree.fromstring(document_xml.encode())
        element_tree = etree.ElementTree(element)
        target_element = element_tree.find("nest").find("android.widget.TextView")
        expected_widget = {
            "selector": "id",
            "selectorValue": "android:id/title",
            "description": "Display Preferences",
            "type": "TextView",
            "state": "enabled"
        }
        actual_widget = abstraction.create_ui_widget(element_tree, target_element)
        self.assertEqual(expected_widget, actual_widget)

    def test_get_widget_state_disabled(self):
        element_xml = """<android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/>"""
        element = etree.fromstring(element_xml)
        widget_state = abstraction._get_widget_state(element)
        self.assertEqual(widget_state, "disabled")

    def test_get_widget_state_enabled(self):
        element_xml = """<android.widget.TextView index="0" text="Show Note Templates" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[48,354][400,403]" resource-id="android:id/title" instance="4"/>"""
        element = etree.fromstring(element_xml)
        widget_state = abstraction._get_widget_state(element)
        self.assertEqual(widget_state, "enabled")

    def test_get_widget_type(self):
        element_xml = """<android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/>"""
        element = etree.fromstring(element_xml)
        widget_type = abstraction._get_widget_type(element)
        self.assertEqual(widget_type, "TextView")

    def test_get_widget_description_with_text_property(self):
        element_xml = """<android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/>"""
        element = etree.fromstring(element_xml)
        widget_description = abstraction._get_widget_description(element)
        self.assertEqual(widget_description, "Display Preferences")

    def test_get_widget_description_with_context_desc(self):
        element_xml = """<android.widget.TextView index="0" text="" class="android.widget.TextView" package="org.tomdroid" content-desc="Display Preferences" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/>"""
        element = etree.fromstring(element_xml)
        widget_description = abstraction._get_widget_description(element)
        self.assertEqual(widget_description, "Display Preferences")

    def test_get_widget_description_with_no_text_or_content_desc(self):
        element_xml = """<android.widget.TextView index="0" text="" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/>"""
        element = etree.fromstring(element_xml)
        widget_description = abstraction._get_widget_description(element)
        self.assertEqual(widget_description, "")

    def test_get_widget_selector_with_unique_id(self):
        document_xml = """<?xml version="1.0" encoding="UTF-8"?>
                            <hierarchy rotation="0"><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                            <nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/></nest>
                            <android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/></hierarchy>"""
        element = etree.fromstring(document_xml.encode())
        element_tree = etree.ElementTree(element)
        element_to_select = element_tree.find("nest").find("android.widget.TextView")
        widget_selector = abstraction._get_widget_selector(element_tree, element_to_select)
        self.assertEqual(widget_selector, ("id", "android:id/title"))

    def test_get_widget_selector_with_non_unique_id(self):
        document_xml = """<?xml version="1.0" encoding="UTF-8"?>
                            <hierarchy rotation="0"><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/>
                            <nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/></nest>
                            <android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/></hierarchy>"""
        element = etree.fromstring(document_xml.encode())
        element_tree = etree.ElementTree(element)
        element_to_select = element_tree.find("nest").find("android.widget.TextView")
        widget_selector = abstraction._get_widget_selector(element_tree, element_to_select)
        self.assertEqual(widget_selector[0], "xpath")

    def test_get_multiple_elements_with_same_id(self):
        document_xml = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/>
                        <nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/></nest>
                        <android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/></hierarchy>"""
        element = etree.fromstring(document_xml.encode())
        element_tree = etree.ElementTree(element)
        resource_id = "android:id/title"
        elements_with_same_id = abstraction._get_elements_with_id(resource_id, element_tree)
        self.assertEqual(len(elements_with_same_id), 3)

    def test_get_single_element_with_id(self):
        document_xml = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                            <nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title" instance="1"/></nest>
                            <android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/></hierarchy>"""
        element = etree.fromstring(document_xml.encode())
        element_tree = etree.ElementTree(element)
        resource_id = "android:id/title"
        elements_with_same_id = abstraction._get_elements_with_id(resource_id, element_tree)
        self.assertEqual(len(elements_with_same_id), 1)

    def test_synthesize(self):
        partial_event = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/title",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }
        current_state = {
            "activityName": "contactsActivity",
            "stateId": "fedcba"
        }
        expected_complete_event = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/title",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            },
            "postcondition": {
                "activityName": "contactsActivity",
                "stateId": "fedcba"
            }
        }
        actual_complete_event = abstraction.synthesize(partial_event, current_state)
        self.assertEqual(expected_complete_event, actual_complete_event)

    def test_create_state(self):
        expected_state = {
            "activityName": "contactsActivity",
            "stateId": "abcdef",
        }
        actual_state = abstraction.create_state("contactsActivity", "abcdef")
        self.assertEqual(actual_state, expected_state)

    def test_create_crash_state(self):
        expected_state = {
            "activityName": "crash",
            "stateId": "crash"
        }
        actual_state = abstraction.create_crash_state()
        self.assertEqual(actual_state, expected_state)

    def test_create_target(self):
        expected_target = {
            "selector": "selector_type",
            "selectorValue": "selector_value",
            "description": "description",
            "type": "type",
            "state": "enabled"
        }
        actual_target = abstraction.create_target("selector_type", "selector_value", "description", "type", "enabled")
        self.assertEqual(expected_target, actual_target)

    def test_create_back_event(self):
        precondition = abstraction.create_state("contactsActivity", "abcdef")
        expected_event = {
            "precondition": precondition,
            "actions": [{
                "target": {
                    "selector": "key_code",
                    "selectorValue": "4",
                    "type": "nav",
                    "description": "back",
                    "state": "enabled"
                },
                "type": "back",
                "value": None
            }]
        }
        actual_event = abstraction.create_back_event(precondition)
        self.maxDiff = None
        self.assertEqual(expected_event, actual_event)

    def test_create_home_event(self):
        precondition = abstraction.create_state("contactsActivity", "abcdef")
        expected_event = {
            "precondition": precondition,
            "actions": [{
                "target": {
                    "selector": "key_code",
                    "selectorValue": "3",
                    "type": "nav",
                    "description": "home",
                    "state": "enabled"
                },
                "type": "home",
                "value": None
            }]
        }
        actual_event = abstraction.create_home_event(precondition)
        self.assertEqual(expected_event, actual_event)

    def test_create_partial_event(self):
        # Arrange
        precondition = abstraction.create_state("contactsActivity", "abcdef")
        actions = [
            {
                "target": {
                    "selector": "id",
                    "selectorValue": "delete_btn",
                    "type": "button",
                    "description": "Delete",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }
        ]

        # Act
        partial_event = abstraction.create_partial_event(precondition, actions)

        # Assert
        expected_event = {
            "precondition": precondition,
            "actions": actions
        }
        self.assertEqual(partial_event, expected_event)

    def test_action_pairs_with_text_entry(self):
        # Arrange
        non_text_entry_action = {
            "target": {
                "selector": "id",
                "selectorValue": "delete_btn",
                "type": "button",
                "description": "Delete",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }

        # Act
        action_pairs_with_text_entry = abstraction.does_action_pair_with_text_entry(non_text_entry_action)

        # Assert
        self.assertTrue(action_pairs_with_text_entry)

    def test_action_does_not_pair_with_text_entry(self):
        # Arrange
        non_pair_action = {
            "target": {
                "selector": "id",
                "selectorValue": "gender_radio_btn",
                "type": "radiobutton",
                "description": "Gender",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }

        # Act
        action_pairs_with_text_entry = abstraction.does_action_pair_with_text_entry(non_pair_action)

        # Assert
        self.assertFalse(action_pairs_with_text_entry)

    def test_pair_text_entry_with_enter_key(self):
        # Arrange
        current_state = abstraction.create_state("contactsActivity", "abcdef")
        text_entry_action = {
            "target": {
                "selector": "id",
                "selectorValue": "txt_first_name",
                "type": "edittext",
                "description": "First Name",
                "state": "enabled"
            },
            "type": "text-entry",
            "value": None
        }

        # Act
        text_entry_enter_key_event = abstraction.pair_text_entry_with_enter_key(current_state, text_entry_action)

        # Assert
        enter_target = abstraction.create_enter_target()
        enter_key_action = abstraction.create_action("enter", enter_target)
        expected_event = {
            "precondition": current_state,
            "actions": [text_entry_action, enter_key_action]
        }
        # self.assertEqual(text_entry_enter_key_event["actions"][0]["value"], "[random string]")
        self.assertEqual(text_entry_enter_key_event, expected_event)

    def test_pair_text_entry_with_non_text_entry_actions(self):
        # Arrange
        current_state = abstraction.create_state("contactsActivity", "abcdef")
        text_entry_action = {
            "target": {
                "selector": "id",
                "selectorValue": "txt_first_name",
                "type": "edittext",
                "description": "First Name",
                "state": "enabled"
            },
            "type": "text-entry",
            "value": None
        }
        action_1 = {
            "target": {
                "selector": "id",
                "selectorValue": "ok_btn",
                "type": "button",
                "description": "OK",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_2 = {
            "target": {
                "selector": "id",
                "selectorValue": "cancel_btn",
                "type": "button",
                "description": "Cancel",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_3 = {
            "target": {
                "selector": "id",
                "selectorValue": "gender_radio_btn",
                "type": "radiobutton",
                "description": "Gender",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }

        non_text_entry_actions = [action_1, action_2, action_3]

        # Act
        text_and_act_events = abstraction.pair_text_entry_with_non_text_entry_actions(current_state,
                                                                                      text_entry_action,
                                                                                      non_text_entry_actions)

        # Assert
        expected_event_1 = {
            "precondition": current_state,
            "actions": [text_entry_action, action_1]
        }
        expected_event_2 = {
            "precondition": current_state,
            "actions": [text_entry_action, action_2]
        }
        expected_events = [expected_event_1, expected_event_2]
        self.assertEqual(text_and_act_events, expected_events)

    def test_create_events_for_single_text_field(self):
        # Arrange
        current_state = abstraction.create_state("contactsActivity", "abcdef")
        text_entry_action = {
            "target": {
                "selector": "id",
                "selectorValue": "txt_first_name",
                "type": "edittext",
                "description": "First Name",
                "state": "enabled"
            },
            "type": "text-entry",
            "value": None
        }
        action_1 = {
            "target": {
                "selector": "id",
                "selectorValue": "ok_btn",
                "type": "button",
                "description": "OK",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_2 = {
            "target": {
                "selector": "id",
                "selectorValue": "cancel_btn",
                "type": "button",
                "description": "Cancel",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_3 = {
            "target": {
                "selector": "id",
                "selectorValue": "gender_radio_btn",
                "type": "radiobutton",
                "description": "Gender",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }

        non_text_entry_actions = [action_1, action_2, action_3]

        # Act
        text_and_act_events = abstraction.create_events_for_single_text_field(current_state, text_entry_action,
                                                                              non_text_entry_actions)

        # Assert
        text_entry_action["value"] = "[random string]"
        expected_event_1 = {
            "precondition": current_state,
            "actions": [text_entry_action, action_1]
        }
        expected_event_2 = {
            "precondition": current_state,
            "actions": [text_entry_action, action_2]
        }
        expected_event_3 = {
            "precondition": current_state,
            "actions": [text_entry_action, abstraction.create_action("enter", abstraction.create_enter_target())]
        }
        expected_events = [expected_event_1, expected_event_2, expected_event_3]
        self.assertEqual(expected_events, text_and_act_events)
        self.assertEqual(text_and_act_events[0]["actions"][0]["value"], "[random string]")

    @unittest.skip
    def test_create_events_for_multiple_text_fields(self):
        # Arrange
        current_state = abstraction.create_state("contactsActivity", "abcdef")
        text_entry_actions = [
            {
                "target": {
                    "selector": "id",
                    "selectorValue": "txt_first_name",
                    "type": "edittext",
                    "description": "First Name",
                    "state": "enabled"
                },
                "type": "text-entry",
                "value": None
            },
            {
                "target": {
                    "selector": "id",
                    "selectorValue": "txt_last_name",
                    "type": "edittext",
                    "description": "Last Name",
                    "state": "enabled"
                },
                "type": "text-entry",
                "value": None
            }
        ]
        action_1 = {
            "target": {
                "selector": "id",
                "selectorValue": "ok_btn",
                "type": "button",
                "description": "OK",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_2 = {
            "target": {
                "selector": "id",
                "selectorValue": "cancel_btn",
                "type": "button",
                "description": "Cancel",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_3 = {
            "target": {
                "selector": "id",
                "selectorValue": "gender_radio_btn",
                "type": "radiobutton",
                "description": "Gender",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }

        non_text_entry_actions = [action_1, action_2, action_3]

        # Act
        text_and_act_events = abstraction.create_events_for_single_text_field(current_state, text_entry_actions,
                                                                              non_text_entry_actions)

        # Assert
        text_entry_actions[0]["value"] = "[random string]"
        text_entry_actions[1]["value"] = "[random string]"
        expected_event_1 = {
            "precondition": current_state,
            "actions": text_entry_actions + [action_1]
        }
        expected_event_2 = {
            "precondition": current_state,
            "actions": text_entry_actions + [action_2]
        }
        expected_events = [expected_event_1, expected_event_2]
        self.assertEqual(expected_events, text_and_act_events)
        self.assertEqual(text_and_act_events[0]["actions"][0]["value"], "[random string]")
        self.assertEqual(text_and_act_events[1]["actions"][0]["value"], "[random string]")

    def test_create_single_action_events(self):
        # Arrange
        current_state = abstraction.create_state("contactsActivity", "abcdef")
        action_1 = {
            "target": {
                "selector": "id",
                "selectorValue": "ok_btn",
                "type": "button",
                "description": "OK",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_2 = {
            "target": {
                "selector": "id",
                "selectorValue": "cancel_btn",
                "type": "button",
                "description": "Cancel",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_3 = {
            "target": {
                "selector": "id",
                "selectorValue": "gender_radio_btn",
                "type": "radiobutton",
                "description": "Gender",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        non_text_entry_actions = [action_1, action_2, action_3]

        # Act
        single_action_events = abstraction.create_single_action_events(current_state, non_text_entry_actions)

        # Assert
        expected_event_1 = {
            "precondition": current_state,
            "actions": [action_1]
        }
        expected_event_2 = {
            "precondition": current_state,
            "actions": [action_2]
        }
        expected_event_3 = {
            "precondition": current_state,
            "actions": [action_3]
        }
        expected_events = [expected_event_1, expected_event_2, expected_event_3]
        self.assertEqual(expected_events, single_action_events)

    def test_create_partial_text_events_with_single_text_field(self):
        # Arrange
        current_state = abstraction.create_state("contactsActivity", "abcdef")
        text_entry_actions = [
            {
                "target": {
                    "selector": "id",
                    "selectorValue": "txt_first_name",
                    "type": "edittext",
                    "description": "First Name",
                    "state": "enabled"
                },
                "type": "text-entry",
                "value": None
            }
        ]
        action_1 = {
            "target": {
                "selector": "id",
                "selectorValue": "ok_btn",
                "type": "button",
                "description": "OK",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_2 = {
            "target": {
                "selector": "id",
                "selectorValue": "cancel_btn",
                "type": "button",
                "description": "Cancel",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_3 = {
            "target": {
                "selector": "id",
                "selectorValue": "gender_radio_btn",
                "type": "radiobutton",
                "description": "Gender",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        non_text_entry_actions = [action_1, action_2, action_3]

        # Act
        partial_text_events = abstraction.create_partial_text_events(current_state, text_entry_actions,
                                                                     non_text_entry_actions)

        # Assert - potentially improve tests to not assert on lists but use membership assert
        text_entry_action = text_entry_actions[0]
        text_entry_action["value"] = "[random string]"
        enter_action = abstraction.create_action("enter", abstraction.create_enter_target())
        expected_event_1 = {
            "precondition": current_state,
            "actions": [text_entry_action, action_1]
        }
        expected_event_2 = {
            "precondition": current_state,
            "actions": [text_entry_action, action_2]
        }
        expected_event_3 = {
            "precondition": current_state,
            "actions": [text_entry_action, enter_action]
        }
        expected_event_4 = {
            "precondition": current_state,
            "actions": [action_1]
        }
        expected_event_5 = {
            "precondition": current_state,
            "actions": [action_2]
        }
        expected_event_6 = {
            "precondition": current_state,
            "actions": [action_3]
        }
        expected_events = [expected_event_1, expected_event_2, expected_event_3, expected_event_4, expected_event_5,
                           expected_event_6]

        self.assertEqual(partial_text_events, expected_events)

    def test_create_partial_text_events_with_multiple_text_fields(self):
        # Arrange
        current_state = abstraction.create_state("contactsActivity", "abcdef")
        text_entry_actions = [
            {
                "target": {
                    "selector": "id",
                    "selectorValue": "txt_first_name",
                    "type": "edittext",
                    "description": "First Name",
                    "state": "enabled"
                },
                "type": "text-entry",
                "value": None
            },
            {
                "target": {
                    "selector": "id",
                    "selectorValue": "txt_last_name",
                    "type": "edittext",
                    "description": "Last Name",
                    "state": "enabled"
                },
                "type": "text-entry",
                "value": None
            }
        ]
        action_1 = {
            "target": {
                "selector": "id",
                "selectorValue": "ok_btn",
                "type": "button",
                "description": "OK",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_2 = {
            "target": {
                "selector": "id",
                "selectorValue": "cancel_btn",
                "type": "button",
                "description": "Cancel",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        action_3 = {
            "target": {
                "selector": "id",
                "selectorValue": "gender_radio_btn",
                "type": "radiobutton",
                "description": "Gender",
                "state": "enabled"
            },
            "type": "click",
            "value": None
        }
        non_text_entry_actions = [action_1, action_2, action_3]

        # Act
        events = abstraction.create_partial_text_events(current_state, text_entry_actions, non_text_entry_actions)

        # Assert
        expected_event_1 = {
            "precondition": current_state,
            "actions": text_entry_actions + [action_1]
        }
        expected_event_2 = {
            "precondition": current_state,
            "actions": text_entry_actions + [action_2]
        }
        expected_event_3 = {
            "precondition": current_state,
            "actions": [action_1]
        }
        expected_event_4 = {
            "precondition": current_state,
            "actions": [action_2]
        }
        expected_event_5 = {
            "precondition": current_state,
            "actions": [action_3]
        }
        expected_events = [expected_event_1, expected_event_2, expected_event_3, expected_event_4, expected_event_5]
        self.assertEqual(expected_events, events)
