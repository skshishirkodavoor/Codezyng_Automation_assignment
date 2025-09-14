"""
Configuration Reader for handling config files
"""
import configparser
import os
from pathlib import Path
from loguru import logger


class ConfigReader:
    """Reads configuration from config.ini and environment variables"""
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = Path(__file__).parent.parent / "config" / "config.ini"
        self.load_config()
    
    def load_config(self):
        """Load configuration from config.ini"""
        try:
            self.config.read(self.config_path)
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise
    
    def get_base_url(self):
        """Get base URL from config"""
        return self.config.get('ENVIRONMENT', 'base_url')
    
    def get_browser(self):
        """Get browser from config"""
        return self.config.get('ENVIRONMENT', 'browser')
    
    def get_headless(self):
        """Get headless mode from config"""
        return self.config.getboolean('ENVIRONMENT', 'headless')
    
    def get_implicit_wait(self):
        """Get implicit wait time"""
        return self.config.getint('ENVIRONMENT', 'implicit_wait')
    
    def get_explicit_wait(self):
        """Get explicit wait time"""
        return self.config.getint('ENVIRONMENT', 'explicit_wait')
    
    def get_page_load_timeout(self):
        """Get page load timeout"""
        return self.config.getint('ENVIRONMENT', 'page_load_timeout')
    
    def get_valid_credentials(self):
        """Get valid login credentials"""
        return {
            'username': self.config.get('CREDENTIALS', 'valid_username'),
            'password': self.config.get('CREDENTIALS', 'valid_password')
        }
    
    def get_invalid_credentials(self):
        """Get invalid login credentials"""
        return {
            'username': self.config.get('CREDENTIALS', 'invalid_username'),
            'password': self.config.get('CREDENTIALS', 'invalid_password')
        }
    
    def get_test_data_file(self):
        """Get test data file path"""
        return self.config.get('TEST_DATA', 'test_data_file')
    
    def get_screenshot_path(self):
        """Get screenshot directory path"""
        return self.config.get('TEST_DATA', 'screenshot_path')
    
    def get_report_path(self):
        """Get report directory path"""
        return self.config.get('TEST_DATA', 'report_path')
    
    def get_max_workers(self):
        """Get maximum workers for parallel execution"""
        return self.config.getint('PARALLEL', 'max_workers')
    
    def is_parallel_enabled(self):
        """Check if parallel execution is enabled"""
        return self.config.getboolean('PARALLEL', 'parallel_tests')
    
    def get_allure_results_path(self):
        """Get Allure results directory path"""
        return self.config.get('REPORTING', 'allure_results')
    
    def get_html_report_path(self):
        """Get HTML report directory path"""
        return self.config.get('REPORTING', 'html_report')