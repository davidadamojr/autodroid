import logging
import random
import time
from appiumatic.constants import *
from exceptions import UnknownAction, EventExecutionFailed
from appium.webdriver.common.touch_action import TouchAction

logger = logging.getLogger(__name__)


# TODO: write tests for the executor after refactoring
class Executor(object):
    def __init__(self, driver, event_interval, text_values):
        self.driver = driver
        self.event_interval = event_interval
        self.text_values = text_values

    def execute(self, event):
        actions = event["actions"]
        for action in actions:
            self.perform(action)

        time.sleep(self.event_interval)

    def perform(self, action):
        target = action["target"]
        action_type = action["type"]

        # TODO: Refactor this - make action classes - may need event classes too - use polymorphism
        # TODO: properly group constants using classes e.g. ActionType.LONG_CLICK
        if action_type == GUIAction.TEXT_ENTRY:
            fill_text(action, self.text_values)
            text_value = action["value"]
            self.type_text(target, text_value)
        elif action_type == GUIAction.HOME_NAV:
            logger.info("Pressing HOME navigation button.")
            self.driver.press_keycode(KeyCode.HOME)
        elif action_type == GUIAction.BACK_NAV:
            logger.info("Pressing BACK navigation button.")
            self.driver.press_keycode(KeyCode.BACK)
        elif action_type == GUIAction.ENTER_KEY:
            logger.info("Pressing RETURN key.")
            self.driver.press_keycode(KeyCode.RETURN)
        elif action_type == SystemAction.RUN_IN_BACKGROUND:
            logger.info("Running app in background for 1 second.")
            self.driver.background_app(1)
        else:
            selector = target["selector"]
            selector_value = target["selectorValue"]
            if selector == SelectorType.ID:
                element = self.driver.find_element_by_id(selector_value)
            else:
                element = self.driver.find_element_by_xpath(selector_value)

            if action_type == GUIAction.LONG_CLICK:
                self.long_click(element)
            elif action_type == GUIAction.SWIPE_UP:
                self.swipe_up()
            elif action_type == GUIAction.SWIPE_DOWN:
                self.swipe_down()
            elif action_type == GUIAction.SWIPE_RIGHT:
                self.swipe_right()
            elif action_type == GUIAction.SWIPE_LEFT:
                self.swipe_left()
            elif action_type == GUIAction.CLICK or action_type == GUIAction.CHECK or \
                    action_type == GUIAction.UNCHECK:
                element.click()
            else:
                raise EventExecutionFailed("Unknown action type.")

    def type_text(self, target, text_value):
        selector = target["selector"]
        selector_value = target["selectorValue"]
        logger.info("Filling in text field: {}".format(selector_value))
        if selector == SelectorType.ID:
            text_entry_element = self.driver.find_element_by_id(selector_value)
        else:
            text_entry_element = self.driver.find_element_by_xpath(selector_value)

        logger.info("Typing text: {}".format(text_value))
        text_entry_element.send_keys(text_value)

    def long_click(self, element):
        logger.info("Executing long-click event.")
        action = TouchAction(self.driver)
        action.long_press(element).perform()

    def swipe_up(self):
        logger.info("Executing swipe up event.")
        screen_size = self.driver.get_window_size()
        start_y = int(screen_size["height"] * 0.80)
        end_y = int(screen_size["height"] * 0.20)
        start_x = int(screen_size["width"] / 2)
        self.driver.swipe(start_x, start_y, start_x, end_y, 200)

    def swipe_down(self):
        logger.info("Executing swipe down event.")
        screen_size = self.driver.get_window_size()
        start_y = int(screen_size["height"] * 0.20)
        end_y = int(screen_size["height"] * 0.80)
        start_x = int(screen_size["width"] / 2)
        self.driver.swipe(start_x, start_y, start_x, end_y, 200)

    def swipe_right(self):
        logger.info("Executing swipe right event.")
        screen_size = self.driver.get_window_size()
        start_x = int(screen_size["width"] * 0.20)
        end_x = int(screen_size["width"] * 0.80)
        start_y = int(screen_size["height"] / 2)

        self.driver.swipe(start_x, start_y, end_x, start_y, 200)

    def swipe_left(self):
        logger.info("Executing swipe left event.")
        screen_size = self.driver.get_window_size()
        start_x = int(screen_size["width"] * 0.80)
        end_x = int(screen_size["width"] * 0.20)
        start_y = int(screen_size["height"] / 2.0)
        self.driver.swipe(start_x, start_y, end_x, start_y, 200)


def fill_text(action, text_values):
    selected_text_value = random.choice(text_values)
    action["value"] = selected_text_value




