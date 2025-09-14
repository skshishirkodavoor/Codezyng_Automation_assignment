"""
Wait utilities for handling dynamic elements
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger
import time


class WaitUtils:
    """Utility class for handling various wait scenarios"""
    
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element {locator} is visible")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not visible within {wait_time} seconds")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable(locator))
            logger.debug(f"Element {locator} is clickable")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not clickable within {wait_time} seconds")
            raise
    
    def wait_for_element_present(self, locator, timeout=None):
        """Wait for element to be present in DOM"""
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"Element {locator} is present")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not present within {wait_time} seconds")
            raise
    
    def wait_for_text_to_be_present_in_element(self, locator, text, timeout=None):
        """Wait for specific text to be present in element"""
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.text_to_be_present_in_element(locator, text))
            logger.debug(f"Text '{text}' found in element {locator}")
            return True
        except TimeoutException:
            logger.error(f"Text '{text}' not found in element {locator} within {wait_time} seconds")
            raise
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """Wait for URL to contain specific text"""
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.url_contains(url_fragment))
            logger.debug(f"URL contains '{url_fragment}'")
            return True
        except TimeoutException:
            logger.error(f"URL does not contain '{url_fragment}' within {wait_time} seconds")
            raise
    
    def wait_for_alert(self, timeout=None):
        """Wait for alert to be present"""
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            alert = wait.until(EC.alert_is_present())
            logger.debug("Alert is present")
            return alert
        except TimeoutException:
            logger.error(f"Alert not present within {wait_time} seconds")
            raise
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear"""
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.invisibility_of_element_located(locator))
            logger.debug(f"Element {locator} has disappeared")
            return True
        except TimeoutException:
            logger.error(f"Element {locator} did not disappear within {wait_time} seconds")
            raise
    
    def fluent_wait(self, locator, timeout=30, poll_frequency=0.5):
        """Fluent wait with custom polling frequency"""
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
            element = wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"Element {locator} found with fluent wait")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not found with fluent wait")
            raise
    
    def custom_retry_wait(self, locator, max_attempts=5, delay=2):
        """Custom retry wait with multiple attempts"""
        for attempt in range(max_attempts):
            try:
                element = self.driver.find_element(*locator)
                if element.is_displayed():
                    logger.debug(f"Element {locator} found on attempt {attempt + 1}")
                    return element
            except NoSuchElementException:
                pass
            
            logger.debug(f"Attempt {attempt + 1} failed, retrying in {delay} seconds...")
            time.sleep(delay)
        
        logger.error(f"Element {locator} not found after {max_attempts} attempts")
        raise NoSuchElementException(f"Element {locator} not found after {max_attempts} attempts")
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to load completely"""
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            logger.debug("Page loaded completely")
            return True
        except TimeoutException:
            logger.error(f"Page did not load completely within {wait_time} seconds")
            raise
