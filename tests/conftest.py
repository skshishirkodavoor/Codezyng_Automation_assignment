"""
Pytest configuration and fixtures
"""
import pytest
import os
from pathlib import Path
from selenium import webdriver
from loguru import logger

from utils.driver_manager import DriverManager
from utils.config_reader import ConfigReader
from utils.screenshot_utils import ScreenshotUtils
from utils.wait_utils import WaitUtils


# Global configuration
config = ConfigReader()


@pytest.fixture(scope="session")
def test_config():
    """Session-level configuration fixture"""
    return config


@pytest.fixture(scope="function")
def driver():
    """Function-level driver fixture"""
    driver_manager = DriverManager(
        browser=config.get_browser(),
        headless=config.get_headless()
    )
    
    driver = driver_manager.get_driver()
    driver.get(config.get_base_url())
    
    yield driver
    
    # Cleanup
    driver.quit()
    logger.info("Driver quit successfully")


@pytest.fixture(scope="function")
def wait_utils(driver):
    """Wait utilities fixture"""
    return WaitUtils(driver, config.get_explicit_wait())


@pytest.fixture(scope="function")
def screenshot_utils(driver):
    """Screenshot utilities fixture"""
    return ScreenshotUtils(driver, config.get_screenshot_path())


@pytest.fixture(scope="function")
def base_test(driver, wait_utils, screenshot_utils):
    """Base test fixture combining all utilities"""
    return BaseTest(driver, wait_utils, screenshot_utils)


class BaseTest:
    """Base test class with common functionality"""
    
    def __init__(self, driver, wait_utils, screenshot_utils):
        self.driver = driver
        self.wait_utils = wait_utils
        self.screenshot_utils = screenshot_utils
        self.config = config
    
    def navigate_to_url(self, url):
        """Navigate to specific URL"""
        try:
            self.driver.get(url)
            self.wait_utils.wait_for_page_load()
            logger.info(f"Navigated to: {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.wait_utils.wait_for_page_load()
        logger.info("Page refreshed")
    
    def go_back(self):
        """Go back to previous page"""
        self.driver.back()
        self.wait_utils.wait_for_page_load()
        logger.info("Navigated back")
    
    def go_forward(self):
        """Go forward to next page"""
        self.driver.forward()
        self.wait_utils.wait_for_page_load()
        logger.info("Navigated forward")
    
    def switch_to_window(self, window_index=0):
        """Switch to specific window"""
        try:
            windows = self.driver.window_handles
            if window_index < len(windows):
                self.driver.switch_to.window(windows[window_index])
                logger.info(f"Switched to window {window_index}")
            else:
                logger.error(f"Window index {window_index} not found")
        except Exception as e:
            logger.error(f"Failed to switch window: {str(e)}")
            raise
    
    def close_current_window(self):
        """Close current window"""
        self.driver.close()
        logger.info("Current window closed")
    
    def switch_to_alert(self):
        """Switch to alert and return alert object"""
        try:
            alert = self.wait_utils.wait_for_alert()
            logger.info("Switched to alert")
            return alert
        except Exception as e:
            logger.error(f"Failed to switch to alert: {str(e)}")
            raise
    
    def accept_alert(self):
        """Accept alert"""
        try:
            alert = self.switch_to_alert()
            alert.accept()
            logger.info("Alert accepted")
        except Exception as e:
            logger.error(f"Failed to accept alert: {str(e)}")
            raise
    
    def dismiss_alert(self):
        """Dismiss alert"""
        try:
            alert = self.switch_to_alert()
            alert.dismiss()
            logger.info("Alert dismissed")
        except Exception as e:
            logger.error(f"Failed to dismiss alert: {str(e)}")
            raise
    
    def get_alert_text(self):
        """Get alert text"""
        try:
            alert = self.switch_to_alert()
            text = alert.text
            logger.info(f"Alert text: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get alert text: {str(e)}")
            raise
    
    def send_keys_to_alert(self, text):
        """Send keys to alert"""
        try:
            alert = self.switch_to_alert()
            alert.send_keys(text)
            logger.info(f"Sent keys to alert: {text}")
        except Exception as e:
            logger.error(f"Failed to send keys to alert: {str(e)}")
            raise


# Pytest hooks
def pytest_configure(config):
    """Configure pytest"""
    # Setup logging
    logger.add(
        "tests/reports/test.log",
        rotation="1 day",
        retention="7 days",
        level="DEBUG"
    )


def pytest_runtest_setup(item):
    """Setup before each test"""
    logger.info(f"Starting test: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """Teardown after each test"""
    logger.info(f"Completed test: {item.name}")


def pytest_runtest_makereport(item, call):
    """Generate test report"""
    if call.when == "call":
        if call.excinfo is not None:
            logger.error(f"Test {item.name} failed: {call.excinfo.value}")
        else:
            logger.info(f"Test {item.name} passed")
