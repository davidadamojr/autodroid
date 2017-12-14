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
