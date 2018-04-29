import unittest
import ui_analysis
import abstraction
from constants import *
from unittest.mock import MagicMock


class UIAnalysisTests(unittest.TestCase):

    def test_can_get_available_events_when_only_nav_and_background(self):
        # Arrange
        webdriver_mock = MagicMock(name="webdriver")
        webdriver_mock.page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                        <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                        </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                        </hierarchy>"""
        webdriver_mock.current_activity = "contactsActivity"
        current_state = ui_analysis.get_current_state(webdriver_mock)

        # Act
        available_events = ui_analysis.get_available_events(webdriver_mock)

        # Assert
        expected_available_events = [
            abstraction.create_back_event(current_state),
            abstraction.create_background_event(current_state)
        ]
        self.assertEqual(available_events, expected_available_events)

    def test_can_get_available_events_with_one_click_event(self):
        # Arrange
        webdriver_mock = MagicMock(name="webdriver")
        webdriver_mock.page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                                <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="false" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                                </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                                </hierarchy>"""
        webdriver_mock.current_activity = "contactsActivity"
        current_state = ui_analysis.get_current_state(webdriver_mock)

        # Act
        available_events = ui_analysis.get_available_events(webdriver_mock)

        # Assert
        expected_available_events = [
            {
                "precondition": current_state,
                "actions": [{
                    "target": abstraction.create_target("id", "android:id/title1", "Display Preferences", TargetType.BUTTON, TargetState.ENABLED),
                    "type": GUIAction.CLICK,
                    "value": None
                }]
            },
            abstraction.create_back_event(current_state),
            abstraction.create_background_event(current_state)
        ]
        self.assertEqual(available_events, expected_available_events)
    
    def test_can_identify_clickable_widgets(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                        <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                        </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                        </hierarchy>"""
        clickable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "Login",
            "type": "TextView",
            "state": "enabled"
        }]
        actual_actionable_widgets = ui_analysis._get_actionable_widgets(page_source)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CLICK]), 2)
        self.assertEqual(clickable_widgets, actual_actionable_widgets[GUIAction.CLICK])
        self.assertEqual(len(actual_actionable_widgets[GUIAction.LONG_CLICK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CHECK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.UNCHECK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_UP]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_DOWN]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_RIGHT]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_LEFT]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.TEXT_ENTRY]), 0)

    def test_can_identify_long_clickable_widgets(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="true" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                            <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="true" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                            </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                            </hierarchy>"""
        long_clickable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "Login",
            "type": "TextView",
            "state": "enabled"
        }]
        actual_actionable_widgets = ui_analysis._get_actionable_widgets(page_source)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.LONG_CLICK]), 2)
        self.assertEqual(long_clickable_widgets, actual_actionable_widgets[GUIAction.LONG_CLICK])
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CLICK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CHECK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.UNCHECK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_UP]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_DOWN]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_RIGHT]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_LEFT]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.TEXT_ENTRY]), 0)

    def test_can_identify_checkable_and_uncheckable_widgets(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="true" checked="true" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                            <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="true" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                            </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                            </hierarchy>"""
        uncheckable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }]
        checkable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "Login",
            "type": "TextView",
            "state": "enabled"
        }]
        actual_actionable_widgets = ui_analysis._get_actionable_widgets(page_source)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.UNCHECK]), 1)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CHECK]), 1)
        self.assertEqual(checkable_widgets, actual_actionable_widgets[GUIAction.CHECK])
        self.assertEqual(uncheckable_widgets, actual_actionable_widgets[GUIAction.UNCHECK])
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CLICK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.LONG_CLICK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_UP]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_DOWN]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.TEXT_ENTRY]), 0)

    def test_can_identify_scrollable_widgets(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="true" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                            <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="true" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                            </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                            </hierarchy>"""
        scrollable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "Login",
            "type": "TextView",
            "state": "enabled"
        }]
        actual_actionable_widgets = ui_analysis._get_actionable_widgets(page_source)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_DOWN]), 2)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_UP]), 2)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_RIGHT]), 2)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_LEFT]), 2)
        self.assertEqual(actual_actionable_widgets[GUIAction.SWIPE_DOWN], scrollable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.SWIPE_UP], scrollable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.SWIPE_LEFT], scrollable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.SWIPE_RIGHT], scrollable_widgets)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CHECK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.UNCHECK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CLICK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.LONG_CLICK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.TEXT_ENTRY]), 0)

    def test_can_identify_enabled_text_input_widgets(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.EditText index="0" text="" class="android.widget.EditText" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                            <nest><android.widget.EditText index="0" text="" class="android.widget.EditText" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                            </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                            </hierarchy>"""
        text_entry_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "",
            "type": "EditText",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "",
            "type": "EditText",
            "state": "enabled"
        }]
        actual_actionable_widgets = ui_analysis._get_actionable_widgets(page_source)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.TEXT_ENTRY]), 2)
        self.assertEqual(actual_actionable_widgets[GUIAction.TEXT_ENTRY], text_entry_widgets)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_DOWN]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_UP]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_RIGHT]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.SWIPE_LEFT]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CHECK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.UNCHECK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.CLICK]), 0)
        self.assertEqual(len(actual_actionable_widgets[GUIAction.LONG_CLICK]), 0)

    def test_can_identify_all_actionable_widget_types(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.EditText index="0" text="" class="android.widget.EditText" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                        <nest><android.widget.CheckBox index="0" text="" class="android.widget.CheckBox" package="org.tomdroid" content-desc="" checkable="true" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                        <android.widget.CheckBox index="0" text="" class="android.widget.CheckBox" package="org.tomdroid" content-desc="" checkable="true" checked="true" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                        </nest><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="true" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title4" instance="1"/>
                        <android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="true" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title5" instance="1"/>
                        </hierarchy>"""
        scrollable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title5",
            "description": "Display Preferences",
            "type": "TextView",
            "state": "enabled"
        }]
        long_clickable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title4",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }]
        checkable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "",
            "type": "CheckBox",
            "state": "enabled"
        }]
        uncheckable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title3",
            "description": "",
            "type": "CheckBox",
            "state": "enabled"
        }]
        text_entry_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "",
            "type": "EditText",
            "state": "enabled"
        }]
        clickable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title4",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }]

        actual_actionable_widgets = ui_analysis._get_actionable_widgets(page_source)
        self.assertEqual(actual_actionable_widgets[GUIAction.CLICK], clickable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.LONG_CLICK], long_clickable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.CHECK], checkable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.UNCHECK], uncheckable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.TEXT_ENTRY], text_entry_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.SWIPE_UP], scrollable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.SWIPE_DOWN], scrollable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.SWIPE_RIGHT], scrollable_widgets)
        self.assertEqual(actual_actionable_widgets[GUIAction.SWIPE_LEFT], scrollable_widgets)

    def test_get_click_actions(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                        <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="true" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                        </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                        </hierarchy>"""
        clickable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "Login",
            "type": "TextView",
            "state": "enabled"
        }]

        expected_actions = [{
            "target": clickable_widgets[0],
            "type": GUIAction.CLICK,
            "value": None
        }, {
            "target": clickable_widgets[1],
            "type": GUIAction.CLICK,
            "value": None
        }]
        actual_actions = ui_analysis.get_possible_actions(page_source)
        self.assertEqual(actual_actions, expected_actions)

    def test_get_long_click_actions(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="true" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                            <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="true" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                            </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                            </hierarchy>"""
        long_clickable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "Login",
            "type": "TextView",
            "state": "enabled"
        }]

        expected_actions = [{
            "target": long_clickable_widgets[0],
            "type": GUIAction.LONG_CLICK,
            "value": None
        }, {
            "target": long_clickable_widgets[1],
            "type": GUIAction.LONG_CLICK,
            "value": None
        }]

        actual_actions = ui_analysis.get_possible_actions(page_source)
        self.assertEqual(actual_actions, expected_actions)

    def test_get_scroll_actions(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="true" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                            <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="true" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                            </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                            </hierarchy>"""

        scrollable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "Login",
            "type": "TextView",
            "state": "enabled"
        }]

        expected_actions = [{
            "target": scrollable_widgets[0],
            "type": GUIAction.SWIPE_DOWN,
            "value": None
        }, {
            "target": scrollable_widgets[0],
            "type": GUIAction.SWIPE_UP,
            "value": None
        }, {
            "target": scrollable_widgets[0],
            "type": GUIAction.SWIPE_RIGHT,
            "value": None
        }, {
            "target": scrollable_widgets[0],
            "type": GUIAction.SWIPE_LEFT,
            "value": None
        }, {
            "target": scrollable_widgets[1],
            "type": GUIAction.SWIPE_DOWN,
            "value": None
        }, {
            "target": scrollable_widgets[1],
            "type": GUIAction.SWIPE_UP,
            "value": None
        }, {
            "target": scrollable_widgets[1],
            "type": GUIAction.SWIPE_RIGHT,
            "value": None
        }, {
            "target": scrollable_widgets[1],
            "type": GUIAction.SWIPE_LEFT,
            "value": None
        }]
        actual_actions = ui_analysis.get_possible_actions(page_source)
        self.assertIn(expected_actions[0], actual_actions)
        self.assertIn(expected_actions[1], actual_actions)
        self.assertIn(expected_actions[2], actual_actions)
        self.assertIn(expected_actions[3], actual_actions)
        self.assertIn(expected_actions[4], actual_actions)
        self.assertIn(expected_actions[5], actual_actions)
        self.assertIn(expected_actions[6], actual_actions)
        self.assertIn(expected_actions[7], actual_actions)

    def test_get_check_actions(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.Button index="0" text="Display Preferences" class="android.widget.Button" package="org.tomdroid" content-desc="" checkable="true" checked="true" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                            <nest><android.widget.TextView index="0" text="Login" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="true" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                            </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                            </hierarchy>"""
        uncheckable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }]
        checkable_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "Login",
            "type": "TextView",
            "state": "enabled"
        }]

        expected_actions = [{
            "target": uncheckable_widgets[0],
            "type": GUIAction.UNCHECK,
            "value": None
        }, {
            "target": checkable_widgets[0],
            "type": GUIAction.CHECK,
            "value": None
        }]
        actual_actions = ui_analysis.get_possible_actions(page_source)
        self.assertIn(expected_actions[0], actual_actions)
        self.assertIn(expected_actions[1], actual_actions)

    def test_get_text_entry_actions(self):
        page_source = """<?xml version="1.0" encoding="UTF-8"?><hierarchy rotation="0"><android.widget.EditText index="0" text="" class="android.widget.EditText" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title1" instance="1"/>
                           <nest><android.widget.EditText index="0" text="" class="android.widget.EditText" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title2" instance="1"/>
                           </nest><android.widget.TextView index="0" text="Display Preferences" class="android.widget.TextView" package="org.tomdroid" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[32,146][736,210]" resource-id="android:id/title3" instance="1"/>
                           </hierarchy>"""
        text_entry_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "",
            "type": "EditText",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "",
            "type": "EditText",
            "state": "enabled"
        }]
        expected_actions = [{
            "target": text_entry_widgets[0],
            "type": GUIAction.TEXT_ENTRY,
            "value": None,
        }, {
            "target": text_entry_widgets[1],
            "type": GUIAction.TEXT_ENTRY,
            "value": None
        }]
        actual_actions = ui_analysis.get_possible_actions(page_source)
        self.assertIn(expected_actions[0], actual_actions)
        self.assertIn(expected_actions[1], actual_actions)

    def test_classify_actions(self):
        text_entry_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/title1",
            "description": "",
            "type": "EditText",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/title2",
            "description": "",
            "type": "EditText",
            "state": "enabled"
        }]

        non_text_entry_widgets = [{
            "selector": "id",
            "selectorValue": "android:id/btn1",
            "description": "Display Preferences",
            "type": "Button",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/btn2",
            "description": "Login",
            "type": "Button",
            "state": "enabled"
        }, {
            "selector": "id",
            "selectorValue": "android:id/checkbox1",
            "description": "Show All",
            "type": "CheckBox",
            "state": "enabled"
        }]

        possible_actions = [
            {
                "target": text_entry_widgets[0],
                "type": GUIAction.TEXT_ENTRY,
                "value": None
            }, {
                "target": text_entry_widgets[1],
                "type": GUIAction.TEXT_ENTRY,
                "value": None
            }, {
                "target": non_text_entry_widgets[0],
                "type": GUIAction.CLICK,
                "value": None
            }, {
                "target": non_text_entry_widgets[1],
                "type":
                    GUIAction.CLICK,
                "value": None
            }, {
                "target": non_text_entry_widgets[2],
                "type": GUIAction.CHECK,
                "value": None
            }, {
                "target": non_text_entry_widgets[2],
                "type": GUIAction.UNCHECK,
                "value": None
            }
        ]

        expected_text_entry_actions = [
            {
                "target": text_entry_widgets[0],
                "type": GUIAction.TEXT_ENTRY,
                "value": None
            }, {
                "target": text_entry_widgets[1],
                "type": GUIAction.TEXT_ENTRY,
                "value": None
            }
        ]

        expected_non_text_entry_actions = [
            {
                "target": non_text_entry_widgets[0],
                "type": GUIAction.CLICK,
                "value": None
            }, {
                "target": non_text_entry_widgets[1],
                "type": GUIAction.CLICK,
                "value": None
            }, {
                "target": non_text_entry_widgets[2],
                "type": GUIAction.CHECK,
                "value": None
            }, {
                "target": non_text_entry_widgets[2],
                "type": GUIAction.UNCHECK,
                "value": None
            }
        ]
        text_entry_actions, non_text_entry_actions = ui_analysis.classify_actions(possible_actions)
        self.assertEqual(text_entry_actions, expected_text_entry_actions)
        self.assertEqual(non_text_entry_actions, expected_non_text_entry_actions)
