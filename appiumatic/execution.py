import logging
import random
from appiumatic import constants
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

    def perform(self, action):
        target = action["target"]
        action_type = action["type"]
        try:
            # TODO: Refactor this - make action classes - may need event classes too - use polymorphism
            # TODO: properly group constants using classes e.g. ActionType.LONG_CLICK
            if action_type == constants.TEXT_ENTRY:
                fill_text(action, self.text_values)
                text_value = action["value"]
                self.type_text(target, text_value)
            elif action_type == constants.HOME_NAV:
                logger.info("Pressing HOME navigation button.")
                self.driver.press_keycode(constants.HOME_KEY_CODE)
            elif action_type == constants.BACK_NAV:
                logger.info("Pressing BACK navigation button.")
                self.driver.press_keycode(constants.BACK_KEY_CODE)
            elif action_type == constants.ENTER_KEY:
                logger.info("Pressing RETURN key.")
                self.driver.press_keycode(constants.ENTER_KEY_CODE)
            else:
                selector = target["selector"]
                selector_value = target["selector_value"]
                if selector == constants.ID_SELECTOR:
                    element = self.driver.find_element_by_id(selector_value)
                else:
                    element = self.driver.find_element_by_xpath(selector_value)

                if action_type == constants.LONG_CLICK:
                    self.long_click(element)
                elif action_type == constants.SCROLL_UP:
                    self.scroll_up()
                elif action_type == constants.SCROLL_DOWN:
                    self.scroll_down()
                elif action_type == constants.CLICK:
                    element.click()
                else:
                    raise EventExecutionFailed("Unknown action type.")
        except Exception as e:
            raise EventExecutionFailed(e.message)

    def type_text(self, target, text_value):
        selector = target["selector"]
        selector_value = target["selector_value"]
        logger.info("Filling in text field: {}".format(selector_value))
        if selector == constants.ID_SELECTOR:
            text_entry_element = self.driver.find_element_by_id(selector_value)
        else:
            text_entry_element = self.driver.find_element_by_xpath(selector_value)

        logger.info("Typing text: {}".format(text_value))
        text_entry_element.set_text(text_value)

    def long_click(self, element):
        logger.info("Executing long-click event.")
        action = TouchAction(self.driver)
        action.long_press(element).perform()

    def scroll_up(self):
        logger.info("Executing scroll up event.")
        screen_size = self.driver.get_window_size()
        start_y = int(screen_size["height"] * 0.80)
        end_y = int(screen_size["height"] * 0.20)
        start_x = int(screen_size["width"] / 2)
        self.driver.swipe(start_x, start_y, start_x, end_y, 200)

    def scroll_down(self):
        logger.info("Executing scroll down event.")
        screen_size = self.driver.get_window_size()
        start_y = int(screen_size["height"] * 0.20)
        end_y = int(screen_size["height"] * 0.80)
        start_x = int(screen_size["width"] / 2)
        self.driver.swipe(start_x, start_y, start_x, end_y, 200)


def fill_text(action, text_values):
    selected_text_value = random.choice(text_values)
    action["value"] = selected_text_value




