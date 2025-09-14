from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from loguru import logger

from utils.wait_utils import WaitUtils
from utils.screenshot_utils import ScreenshotUtils


class BasePage:
    
    def __init__(self, driver: WebDriver, wait_utils: WaitUtils, screenshot_utils: ScreenshotUtils):
        self.driver = driver
        self.wait_utils = wait_utils
        self.screenshot_utils = screenshot_utils
        self.actions = ActionChains(driver)
    
    def find_element(self, locator):
        """one item"""

        try:
            element = self.wait_utils.wait_for_element_visible(locator)
            logger.debug(f"Element found: {locator}")
            return element
        except Exception as e:
            logger.error(f"Element not found: {locator}, Error: {str(e)}")
            raise
    
    def find_elements(self, locator):
        """multiple"""
        try:
            elements = self.driver.find_elements(*locator)
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except Exception as e:
            logger.error(f"Elements not found: {locator}, Error: {str(e)}")
            raise
    
    def click_element(self, locator):
        """Click"""
        try:
            element = self.wait_utils.wait_for_element_clickable(locator)
            element.click()
            logger.info(f"Clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to click element: {locator}, Error: {str(e)}")
            raise
    
    def send_keys_to_element(self, locator, text):
        """Send keys"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"Sent keys '{text}' to element: {locator}")
        except Exception as e:
            logger.error(f"Failed to send keys to element: {locator}, Error: {str(e)}")
            raise
    
    def get_element_text(self, locator):
        """Gettext"""
        try:
            element = self.find_element(locator)
            text = element.text
            logger.debug(f"Element text: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element: {locator}, Error: {str(e)}")
            raise
    
    def get_element_attribute(self, locator, attribute):
        """Get attribute value"""
        try:
            element = self.find_element(locator)
            value = element.get_attribute(attribute)
            logger.debug(f"Element attribute '{attribute}': {value}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute from element: {locator}, Error: {str(e)}")
            raise
    
    def is_element_displayed(self, locator):
        """Check display"""
        try:
            element = self.find_element(locator)
            is_displayed = element.is_displayed()
            logger.debug(f"Element displayed: {is_displayed}")
            return is_displayed
        except Exception:
            logger.debug(f"Element not displayed: {locator}")
            return False
    
    def is_element_enabled(self, locator):
        """Check enabled"""
        try:
            element = self.find_element(locator)
            is_enabled = element.is_enabled()
            logger.debug(f"Element enabled: {is_enabled}")
            return is_enabled
        except Exception:
            logger.debug(f"Element not enabled: {locator}")
            return False
    
    def is_element_selected(self, locator):
        """Check select"""
        try:
            element = self.find_element(locator)
            is_selected = element.is_selected()
            logger.debug(f"Element selected: {is_selected}")
            return is_selected
        except Exception:
            logger.debug(f"Element not selected: {locator}")
            return False
    
    def hover_over_element(self, locator):
        """Hover over element"""
        try:
            element = self.find_element(locator)
            self.actions.move_to_element(element).perform()
            logger.info(f"Hovered over element: {locator}")
        except Exception as e:
            logger.error(f"Failed to hover over element: {locator}, Error: {str(e)}")
            raise
    
    def double_click_element(self, locator):
        """Double click on element"""
        try:
            element = self.find_element(locator)
            self.actions.double_click(element).perform()
            logger.info(f"Double clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to double click element: {locator}, Error: {str(e)}")
            raise
    
    def right_click_element(self, locator):
        """Right click on element"""
        try:
            element = self.find_element(locator)
            self.actions.context_click(element).perform()
            logger.info(f"Right clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to right click element: {locator}, Error: {str(e)}")
            raise
    
    def drag_and_drop(self, source_locator, target_locator):
        """Drag and drop element"""
        try:
            source_element = self.find_element(source_locator)
            target_element = self.find_element(target_locator)
            self.actions.drag_and_drop(source_element, target_element).perform()
            logger.info(f"Dragged element from {source_locator} to {target_locator}")
        except Exception as e:
            logger.error(f"Failed to drag and drop: {str(e)}")
            raise
    
    def scroll_to_element(self, locator):
        """Scroll to element"""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            logger.info(f"Scrolled to element: {locator}")
        except Exception as e:
            logger.error(f"Failed to scroll to element: {locator}, Error: {str(e)}")
            raise
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            logger.info("Scrolled to top of page")
        except Exception as e:
            logger.error(f"Failed to scroll to top: {str(e)}")
            raise
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logger.info("Scrolled to bottom of page")
        except Exception as e:
            logger.error(f"Failed to scroll to bottom: {str(e)}")
            raise
    
    def press_key(self, key):
        """Press a key"""
        try:
            if key.upper() == "ENTER":
                self.actions.send_keys(Keys.ENTER).perform()
            elif key.upper() == "TAB":
                self.actions.send_keys(Keys.TAB).perform()
            elif key.upper() == "ESCAPE":
                self.actions.send_keys(Keys.ESCAPE).perform()
            elif key.upper() == "SPACE":
                self.actions.send_keys(Keys.SPACE).perform()
            else:
                self.actions.send_keys(key).perform()
            logger.info(f"Pressed key: {key}")
        except Exception as e:
            logger.error(f"Failed to press key: {key}, Error: {str(e)}")
            raise
    
    def select_dropdown_option(self, dropdown_locator, option_text):
        """Select option from dropdown by text"""
        try:
            from selenium.webdriver.support.ui import Select
            dropdown = self.find_element(dropdown_locator)
            select = Select(dropdown)
            select.select_by_visible_text(option_text)
            logger.info(f"Selected option '{option_text}' from dropdown: {dropdown_locator}")
        except Exception as e:
            logger.error(f"Failed to select dropdown option: {str(e)}")
            raise
    
    def select_dropdown_option_by_value(self, dropdown_locator, option_value):
        """Select option from dropdown by value"""
        try:
            from selenium.webdriver.support.ui import Select
            dropdown = self.find_element(dropdown_locator)
            select = Select(dropdown)
            select.select_by_value(option_value)
            logger.info(f"Selected option value '{option_value}' from dropdown: {dropdown_locator}")
        except Exception as e:
            logger.error(f"Failed to select dropdown option by value: {str(e)}")
            raise
    
    def wait_for_text_in_element(self, locator, text):
        """Wait for specific text in element"""
        try:
            self.wait_utils.wait_for_text_to_be_present_in_element(locator, text)
            logger.info(f"Text '{text}' found in element: {locator}")
        except Exception as e:
            logger.error(f"Text '{text}' not found in element: {locator}, Error: {str(e)}")
            raise
    
    def wait_for_element_to_disappear(self, locator):
        """Wait for element to disappear"""
        try:
            self.wait_utils.wait_for_element_to_disappear(locator)
            logger.info(f"Element disappeared: {locator}")
        except Exception as e:
            logger.error(f"Element did not disappear: {locator}, Error: {str(e)}")
            raise
    
    def switch_to_iframe(self, iframe_locator):
        """Switch to iframe"""
        try:
            iframe = self.find_element(iframe_locator)
            self.driver.switch_to.frame(iframe)
            logger.info(f"Switched to iframe: {iframe_locator}")
        except Exception as e:
            logger.error(f"Failed to switch to iframe: {str(e)}")
            raise
    
    def switch_to_default_content(self):
        """Switch back to default content"""
        try:
            self.driver.switch_to.default_content()
            logger.info("Switched to default content")
        except Exception as e:
            logger.error(f"Failed to switch to default content: {str(e)}")
            raise
    
    def upload_file(self, file_input_locator, file_path):
        """Upload file"""
        try:
            file_input = self.find_element(file_input_locator)
            file_input.send_keys(file_path)
            logger.info(f"Uploaded file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to upload file: {str(e)}")
            raise
