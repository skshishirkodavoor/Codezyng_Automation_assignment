"""
Screenshot utilities for capturing screenshots
"""
import os
from datetime import datetime
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger


class ScreenshotUtils:
    """Utility class for capturing screenshots"""
    
    def __init__(self, driver: WebDriver, screenshot_dir="tests/screenshots"):
        self.driver = driver
        self.screenshot_dir = Path(screenshot_dir)
        self._create_screenshot_dir()
    
    def _create_screenshot_dir(self):
        """Create screenshot directory if it doesn't exist"""
        try:
            self.screenshot_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Screenshot directory created: {self.screenshot_dir}")
        except Exception as e:
            logger.error(f"Failed to create screenshot directory: {str(e)}")
            raise
    
    def capture_screenshot(self, test_name="test", status="failed"):
        """Capture screenshot with timestamp and test name"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{status}_{timestamp}.png"
            filepath = self.screenshot_dir / filename
            
            # Take screenshot
            self.driver.save_screenshot(str(filepath))
            logger.info(f"Screenshot captured: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")
            raise
    
    def capture_element_screenshot(self, element, test_name="test", status="failed"):
        """Capture screenshot of specific element"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{status}_element_{timestamp}.png"
            filepath = self.screenshot_dir / filename
            
            # Take element screenshot
            element.screenshot(str(filepath))
            logger.info(f"Element screenshot captured: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to capture element screenshot: {str(e)}")
            raise
    
    def capture_full_page_screenshot(self, test_name="test", status="failed"):
        """Capture full page screenshot (including scrollable content)"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{status}_fullpage_{timestamp}.png"
            filepath = self.screenshot_dir / filename
            
            # Get original window size
            original_size = self.driver.get_window_size()
            
            # Get total page dimensions
            total_width = self.driver.execute_script("return document.body.scrollWidth")
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Set window size to full page
            self.driver.set_window_size(total_width, total_height)
            
            # Take screenshot
            self.driver.save_screenshot(str(filepath))
            
            # Restore original window size
            self.driver.set_window_size(original_size['width'], original_size['height'])
            
            logger.info(f"Full page screenshot captured: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to capture full page screenshot: {str(e)}")
            raise
    
    def capture_screenshot_on_failure(self, test_name, exception):
        """Capture screenshot when test fails"""
        try:
            screenshot_path = self.capture_screenshot(test_name, "failed")
            logger.error(f"Test {test_name} failed. Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to capture failure screenshot: {str(e)}")
            return None
    
    def capture_screenshot_on_success(self, test_name):
        """Capture screenshot when test passes (optional)"""
        try:
            screenshot_path = self.capture_screenshot(test_name, "passed")
            logger.info(f"Test {test_name} passed. Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to capture success screenshot: {str(e)}")
            return None
    
    def cleanup_old_screenshots(self, days_old=7):
        """Clean up screenshots older than specified days"""
        try:
            current_time = datetime.now()
            deleted_count = 0
            
            for file_path in self.screenshot_dir.glob("*.png"):
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if (current_time - file_time).days > days_old:
                    file_path.unlink()
                    deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old screenshots")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup old screenshots: {str(e)}")
            return 0
