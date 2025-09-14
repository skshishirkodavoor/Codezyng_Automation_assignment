"""
Login Test Cases
"""
import pytest
from loguru import logger

from tests.pages.login_page import LoginPage
from tests.pages.home_page import HomePage
from utils.data_utils import DataUtils


class TestLogin:
    """Test class for login functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, wait_utils, screenshot_utils):
        """Setup for each test"""
        self.driver = driver
        self.wait_utils = wait_utils
        self.screenshot_utils = screenshot_utils
        self.login_page = LoginPage(driver, wait_utils, screenshot_utils)
        self.home_page = HomePage(driver, wait_utils, screenshot_utils)
        self.data_utils = DataUtils()
    
    def test_valid_login(self, test_config):
        """Test valid login"""
        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            
            # Get valid credentials from config
            credentials = test_config.get_valid_credentials()
            
            # Perform login
            success = self.login_page.login(
                credentials['username'],
                credentials['password']
            )
            
            # Verify login success
            assert success, "Login should be successful"
            assert self.home_page.is_logged_in(), "User should be logged in"
            
            logger.info("Valid login test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_valid_login", e)
            logger.error(f"Valid login test failed: {str(e)}")
            raise
    
    def test_invalid_login(self, test_config):
        """Test invalid login"""
        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            
            # Get invalid credentials from config
            credentials = test_config.get_invalid_credentials()
            
            # Perform login with invalid credentials
            success = self.login_page.login(
                credentials['username'],
                credentials['password']
            )
            
            # Verify login failure
            assert not success, "Login should fail with invalid credentials"
            assert not self.home_page.is_logged_in(), "User should not be logged in"
            
            # Check for error message
            error_message = self.login_page.get_error_message()
            assert error_message is not None, "Error message should be displayed"
            
            logger.info("Invalid login test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_invalid_login", e)
            logger.error(f"Invalid login test failed: {str(e)}")
            raise
    
    @pytest.mark.parametrize("username,password,expected", [
        ("", "demo", "failure"),
        ("demo@opencart.com", "", "failure"),
        ("invalid@test.com", "wrong", "failure"),
        ("demo@opencart.com", "demo", "success")
    ])
    def test_login_data_driven(self, username, password, expected):
        """Test login with data-driven approach"""
        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            
            # Perform login
            success = self.login_page.login(username, password)
            
            if expected == "success":
                assert success, f"Login should succeed for {username}"
                assert self.home_page.is_logged_in(), "User should be logged in"
            else:
                assert not success, f"Login should fail for {username}"
                assert not self.home_page.is_logged_in(), "User should not be logged in"
            
            logger.info(f"Data-driven login test passed for {username}")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_login_data_driven", e)
            logger.error(f"Data-driven login test failed: {str(e)}")
            raise
    
    def test_remember_me_functionality(self, test_config):
        """Test remember me functionality"""
        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            
            # Get valid credentials
            credentials = test_config.get_valid_credentials()
            
            # Perform login with remember me checked
            success = self.login_page.login(
                credentials['username'],
                credentials['password'],
                remember_me=True
            )
            
            # Verify login success
            assert success, "Login should be successful"
            assert self.home_page.is_logged_in(), "User should be logged in"
            
            # Logout
            self.login_page.logout()
            
            # Check if remember me checkbox is still checked (if applicable)
            # Note: This depends on the application's implementation
            
            logger.info("Remember me functionality test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_remember_me", e)
            logger.error(f"Remember me test failed: {str(e)}")
            raise
    
    def test_login_logout_cycle(self, test_config):
        """Test complete login-logout cycle"""
        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            
            # Get valid credentials
            credentials = test_config.get_valid_credentials()
            
            # Login
            success = self.login_page.login(
                credentials['username'],
                credentials['password']
            )
            assert success, "Login should be successful"
            assert self.home_page.is_logged_in(), "User should be logged in"
            
            # Logout
            self.login_page.logout()
            assert not self.home_page.is_logged_in(), "User should be logged out"
            
            logger.info("Login-logout cycle test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_login_logout", e)
            logger.error(f"Login-logout cycle test failed: {str(e)}")
            raise
    
    def test_forgotten_password_link(self):
        """Test forgotten password link"""
        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            
            # Click forgotten password link
            self.login_page.click_forgotten_password_link()
            
            # Verify navigation to forgotten password page
            current_url = self.driver.current_url
            assert "forgotten" in current_url.lower(), "Should navigate to forgotten password page"
            
            logger.info("Forgotten password link test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_forgotten_password", e)
            logger.error(f"Forgotten password test failed: {str(e)}")
            raise
    
    def test_register_link(self):
        """Test register link"""
        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            
            # Click register link
            self.login_page.click_register_link()
            
            # Verify navigation to register page
            current_url = self.driver.current_url
            assert "register" in current_url.lower(), "Should navigate to register page"
            
            logger.info("Register link test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_register_link", e)
            logger.error(f"Register link test failed: {str(e)}")
            raise
