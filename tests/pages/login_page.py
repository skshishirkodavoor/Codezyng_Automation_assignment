"""
Login Page Object Model
"""
from selenium.webdriver.common.by import By
from loguru import logger

from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page class"""
    
    # Locators
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Login']")
    REMEMBER_ME_CHECKBOX = (By.NAME, "remember")
    FORGOTTEN_PASSWORD_LINK = (By.LINK_TEXT, "Forgotten Password")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    ERROR_MESSAGE = (By.CLASS_NAME, "alert-danger")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "alert-success")
    ACCOUNT_DROPDOWN = (By.CSS_SELECTOR, ".dropdown .dropdown-toggle")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    
    def __init__(self, driver, wait_utils, screenshot_utils):
        super().__init__(driver, wait_utils, screenshot_utils)
        self.page_url = "/index.php?route=account/login"
    
    def navigate_to_login_page(self):
        """Navigate to login page"""
        try:
            full_url = self.driver.current_url.split('/')[0] + '//' + self.driver.current_url.split('/')[2] + self.page_url
            self.driver.get(full_url)
            self.wait_utils.wait_for_page_load()
            logger.info("Navigated to login page")
        except Exception as e:
            logger.error(f"Failed to navigate to login page: {str(e)}")
            raise
    
    def enter_email(self, email):
        """Enter email address"""
        try:
            self.send_keys_to_element(self.EMAIL_INPUT, email)
            logger.info(f"Entered email: {email}")
        except Exception as e:
            logger.error(f"Failed to enter email: {str(e)}")
            raise
    
    def enter_password(self, password):
        """Enter password"""
        try:
            self.send_keys_to_element(self.PASSWORD_INPUT, password)
            logger.info("Entered password")
        except Exception as e:
            logger.error(f"Failed to enter password: {str(e)}")
            raise
    
    def click_login_button(self):
        """Click login button"""
        try:
            self.click_element(self.LOGIN_BUTTON)
            logger.info("Clicked login button")
        except Exception as e:
            logger.error(f"Failed to click login button: {str(e)}")
            raise
    
    def check_remember_me(self):
        """Check remember me checkbox"""
        try:
            if not self.is_element_selected(self.REMEMBER_ME_CHECKBOX):
                self.click_element(self.REMEMBER_ME_CHECKBOX)
            logger.info("Checked remember me checkbox")
        except Exception as e:
            logger.error(f"Failed to check remember me: {str(e)}")
            raise
    
    def uncheck_remember_me(self):
        """Uncheck remember me checkbox"""
        try:
            if self.is_element_selected(self.REMEMBER_ME_CHECKBOX):
                self.click_element(self.REMEMBER_ME_CHECKBOX)
            logger.info("Unchecked remember me checkbox")
        except Exception as e:
            logger.error(f"Failed to uncheck remember me: {str(e)}")
            raise
    
    def click_forgotten_password_link(self):
        """Click forgotten password link"""
        try:
            self.click_element(self.FORGOTTEN_PASSWORD_LINK)
            logger.info("Clicked forgotten password link")
        except Exception as e:
            logger.error(f"Failed to click forgotten password link: {str(e)}")
            raise
    
    def click_register_link(self):
        """Click register link"""
        try:
            self.click_element(self.REGISTER_LINK)
            logger.info("Clicked register link")
        except Exception as e:
            logger.error(f"Failed to click register link: {str(e)}")
            raise
    
    def get_error_message(self):
        """Get error message text"""
        try:
            if self.is_element_displayed(self.ERROR_MESSAGE):
                error_text = self.get_element_text(self.ERROR_MESSAGE)
                logger.info(f"Error message: {error_text}")
                return error_text
            return None
        except Exception as e:
            logger.error(f"Failed to get error message: {str(e)}")
            return None
    
    def get_success_message(self):
        """Get success message text"""
        try:
            if self.is_element_displayed(self.SUCCESS_MESSAGE):
                success_text = self.get_element_text(self.SUCCESS_MESSAGE)
                logger.info(f"Success message: {success_text}")
                return success_text
            return None
        except Exception as e:
            logger.error(f"Failed to get success message: {str(e)}")
            return None
    
    def is_login_successful(self):
        """Check if login was successful"""
        try:
            # Check if account dropdown is visible (indicates successful login)
            return self.is_element_displayed(self.ACCOUNT_DROPDOWN)
        except Exception as e:
            logger.error(f"Failed to check login status: {str(e)}")
            return False
    
    def login(self, email, password, remember_me=False):
        """Complete login process"""
        try:
            self.enter_email(email)
            self.enter_password(password)
            
            if remember_me:
                self.check_remember_me()
            
            self.click_login_button()
            
            # Wait for login to complete
            if self.is_login_successful():
                logger.info("Login successful")
                return True
            else:
                logger.warning("Login failed")
                return False
                
        except Exception as e:
            logger.error(f"Login process failed: {str(e)}")
            raise
    
    def logout(self):
        """Logout from account"""
        try:
            # Click account dropdown
            self.click_element(self.ACCOUNT_DROPDOWN)
            
            # Click logout link
            self.click_element(self.LOGOUT_LINK)
            
            logger.info("Logged out successfully")
        except Exception as e:
            logger.error(f"Failed to logout: {str(e)}")
            raise
    
    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            return self.is_element_displayed(self.ACCOUNT_DROPDOWN)
        except Exception:
            return False
    
    def clear_login_form(self):
        """Clear login form fields"""
        try:
            self.find_element(self.EMAIL_INPUT).clear()
            self.find_element(self.PASSWORD_INPUT).clear()
            logger.info("Cleared login form")
        except Exception as e:
            logger.error(f"Failed to clear login form: {str(e)}")
            raise
