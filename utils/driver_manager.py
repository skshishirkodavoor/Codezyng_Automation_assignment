"""
Driver Manager for handling different browsers
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from loguru import logger


class DriverManager:
    """Manages WebDriver instances for different browsers"""
    
    def __init__(self, browser="chrome", headless=False):
        self.browser = browser.lower()
        self.headless = headless
        self.driver = None
        
    def get_driver(self):
        """Initialize and return WebDriver instance"""
        try:
            if self.browser == "chrome":
                self.driver = self._get_chrome_driver()
            elif self.browser == "firefox":
                self.driver = self._get_firefox_driver()
            elif self.browser == "edge":
                self.driver = self._get_edge_driver()
            else:
                raise ValueError(f"Unsupported browser: {self.browser}")
            
            # Set timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(30)
            self.driver.maximize_window()
            
            logger.info(f"Successfully initialized {self.browser} driver")
            return self.driver
            
        except Exception as e:
            logger.error(f"Failed to initialize {self.browser} driver: {str(e)}")
            raise
    
    def _get_chrome_driver(self):
        """Initialize Chrome driver"""
        options = ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        # Additional Chrome options for better stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _get_firefox_driver(self):
        """Initialize Firefox driver"""
        options = FirefoxOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def _get_edge_driver(self):
        """Initialize Edge driver"""
        options = EdgeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    def quit_driver(self):
        """Quit the driver instance"""
        if self.driver:
            self.driver.quit()
            logger.info("Driver quit successfully")