"""
Checkout Test Cases
"""
import pytest
from loguru import logger

from tests.pages.home_page import HomePage
from tests.pages.cart_page import CartPage
from tests.pages.checkout_page import CheckoutPage
from tests.pages.login_page import LoginPage
from utils.data_utils import DataUtils


class TestCheckout:
    """Test class for checkout functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, wait_utils, screenshot_utils):
        """Setup for each test"""
        self.driver = driver
        self.wait_utils = wait_utils
        self.screenshot_utils = screenshot_utils
        self.home_page = HomePage(driver, wait_utils, screenshot_utils)
        self.cart_page = CartPage(driver, wait_utils, screenshot_utils)
        self.checkout_page = CheckoutPage(driver, wait_utils, screenshot_utils)
        self.login_page = LoginPage(driver, wait_utils, screenshot_utils)
        self.data_utils = DataUtils()
    
    def test_guest_checkout(self):
        """Test guest checkout process"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart and proceed to checkout
            self.cart_page.navigate_to_cart()
            self.cart_page.click_checkout()
            
            # Navigate to checkout page
            self.checkout_page.navigate_to_checkout()
            
            # Prepare test data
            billing_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'company': 'Test Company',
                'address_1': '123 Test Street',
                'address_2': 'Apt 1',
                'city': 'Test City',
                'postcode': '12345',
                'country': 'United States',
                'region': 'California'
            }
            
            account_data = {
                'email': 'john.doe@test.com',
                'telephone': '1234567890'
            }
            
            # Complete checkout
            self.checkout_page.complete_checkout(billing_data, account_data)
            
            # Verify order confirmation
            confirmation = self.checkout_page.get_order_confirmation()
            assert confirmation is not None, "Order confirmation should be displayed"
            
            logger.info("Guest checkout test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_guest_checkout", e)
            logger.error(f"Guest checkout test failed: {str(e)}")
            raise
    
    def test_logged_in_user_checkout(self, test_config):
        """Test checkout for logged in user"""
        try:
            # Login first
            self.login_page.navigate_to_login_page()
            credentials = test_config.get_valid_credentials()
            self.login_page.login(credentials['username'], credentials['password'])
            
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart and proceed to checkout
            self.cart_page.navigate_to_cart()
            self.cart_page.click_checkout()
            
            # Navigate to checkout page
            self.checkout_page.navigate_to_checkout()
            
            # Prepare test data
            billing_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'company': 'Test Company',
                'address_1': '123 Test Street',
                'address_2': 'Apt 1',
                'city': 'Test City',
                'postcode': '12345',
                'country': 'United States',
                'region': 'California'
            }
            
            account_data = {
                'email': credentials['username'],
                'telephone': '1234567890'
            }
            
            # Complete checkout
            self.checkout_page.complete_checkout(billing_data, account_data)
            
            # Verify order confirmation
            confirmation = self.checkout_page.get_order_confirmation()
            assert confirmation is not None, "Order confirmation should be displayed"
            
            logger.info("Logged in user checkout test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_logged_in_checkout", e)
            logger.error(f"Logged in user checkout test failed: {str(e)}")
            raise
    
    @pytest.mark.parametrize("payment_method", ["cod", "bank_transfer", "cheque"])
    def test_different_payment_methods(self, payment_method):
        """Test different payment methods"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart and proceed to checkout
            self.cart_page.navigate_to_cart()
            self.cart_page.click_checkout()
            
            # Navigate to checkout page
            self.checkout_page.navigate_to_checkout()
            
            # Prepare test data
            billing_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'address_1': '123 Test Street',
                'city': 'Test City',
                'postcode': '12345',
                'country': 'United States',
                'region': 'California'
            }
            
            account_data = {
                'email': 'john.doe@test.com',
                'telephone': '1234567890'
            }
            
            # Complete checkout with specific payment method
            self.checkout_page.complete_checkout(billing_data, account_data, payment_method)
            
            # Verify order confirmation
            confirmation = self.checkout_page.get_order_confirmation()
            assert confirmation is not None, f"Order confirmation should be displayed for {payment_method}"
            
            logger.info(f"Payment method {payment_method} test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_payment_methods", e)
            logger.error(f"Payment method {payment_method} test failed: {str(e)}")
            raise
    
    def test_checkout_with_different_delivery_address(self):
        """Test checkout with different delivery address"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart and proceed to checkout
            self.cart_page.navigate_to_cart()
            self.cart_page.click_checkout()
            
            # Navigate to checkout page
            self.checkout_page.navigate_to_checkout()
            
            # Fill billing details
            billing_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'address_1': '123 Billing Street',
                'city': 'Billing City',
                'postcode': '12345',
                'country': 'United States',
                'region': 'California'
            }
            
            account_data = {
                'email': 'john.doe@test.com',
                'telephone': '1234567890'
            }
            
            # Fill billing details
            self.checkout_page.fill_billing_details(billing_data)
            self.checkout_page.fill_account_details(account_data)
            self.checkout_page.click_continue()
            
            # Wait for shipping section
            self.wait_utils.wait_for_page_load()
            
            # Uncheck same as billing
            self.checkout_page.uncheck_same_as_billing()
            
            # Fill different delivery details
            delivery_data = {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'address_1': '456 Delivery Street',
                'city': 'Delivery City',
                'postcode': '54321',
                'country': 'United States',
                'region': 'New York'
            }
            
            self.checkout_page.fill_delivery_details(delivery_data)
            self.checkout_page.click_continue_shipping()
            
            # Continue with rest of checkout
            self.wait_utils.wait_for_page_load()
            self.checkout_page.select_shipping_method()
            self.checkout_page.click_continue_shipping_method()
            
            self.wait_utils.wait_for_page_load()
            self.checkout_page.select_payment_method()
            self.checkout_page.accept_terms_and_conditions()
            self.checkout_page.accept_privacy_policy()
            self.checkout_page.click_continue_payment_method()
            
            self.wait_utils.wait_for_page_load()
            self.checkout_page.confirm_order()
            
            # Verify order confirmation
            confirmation = self.checkout_page.get_order_confirmation()
            assert confirmation is not None, "Order confirmation should be displayed"
            
            logger.info("Different delivery address checkout test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_different_delivery", e)
            logger.error(f"Different delivery address test failed: {str(e)}")
            raise
    
    def test_checkout_validation_errors(self):
        """Test checkout form validation"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart and proceed to checkout
            self.cart_page.navigate_to_cart()
            self.cart_page.click_checkout()
            
            # Navigate to checkout page
            self.checkout_page.navigate_to_checkout()
            
            # Try to continue without filling required fields
            self.checkout_page.click_continue()
            
            # Check for validation errors
            error_messages = self.checkout_page.get_error_messages()
            assert len(error_messages) > 0, "Validation errors should be displayed"
            
            logger.info("Checkout validation test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_checkout_validation", e)
            logger.error(f"Checkout validation test failed: {str(e)}")
            raise
    
    def test_checkout_with_newsletter_subscription(self):
        """Test checkout with newsletter subscription"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart and proceed to checkout
            self.cart_page.navigate_to_cart()
            self.cart_page.click_checkout()
            
            # Navigate to checkout page
            self.checkout_page.navigate_to_checkout()
            
            # Prepare test data
            billing_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'address_1': '123 Test Street',
                'city': 'Test City',
                'postcode': '12345',
                'country': 'United States',
                'region': 'California'
            }
            
            account_data = {
                'email': 'john.doe@test.com',
                'telephone': '1234567890'
            }
            
            # Complete checkout with newsletter subscription
            self.checkout_page.fill_billing_details(billing_data)
            self.checkout_page.fill_account_details(account_data)
            self.checkout_page.click_continue()
            
            self.wait_utils.wait_for_page_load()
            self.checkout_page.check_same_as_billing()
            self.checkout_page.click_continue_shipping()
            
            self.wait_utils.wait_for_page_load()
            self.checkout_page.select_shipping_method()
            self.checkout_page.click_continue_shipping_method()
            
            self.wait_utils.wait_for_page_load()
            self.checkout_page.select_payment_method()
            self.checkout_page.accept_terms_and_conditions()
            self.checkout_page.accept_privacy_policy()
            self.checkout_page.subscribe_to_newsletter()
            self.checkout_page.click_continue_payment_method()
            
            self.wait_utils.wait_for_page_load()
            self.checkout_page.confirm_order()
            
            # Verify order confirmation
            confirmation = self.checkout_page.get_order_confirmation()
            assert confirmation is not None, "Order confirmation should be displayed"
            
            logger.info("Newsletter subscription checkout test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_newsletter_checkout", e)
            logger.error(f"Newsletter subscription checkout test failed: {str(e)}")
            raise
    
    def test_checkout_order_total_calculation(self):
        """Test order total calculation during checkout"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart and get total
            self.cart_page.navigate_to_cart()
            cart_total = self.cart_page.get_total()
            
            # Proceed to checkout
            self.cart_page.click_checkout()
            self.checkout_page.navigate_to_checkout()
            
            # Get checkout total
            checkout_total = self.checkout_page.get_order_total()
            
            # Verify totals match
            assert abs(cart_total - checkout_total) < 0.01, \
                f"Cart total {cart_total} should match checkout total {checkout_total}"
            
            logger.info(f"Order total calculation verified: {checkout_total}")
            logger.info("Order total calculation test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_order_total", e)
            logger.error(f"Order total calculation test failed: {str(e)}")
            raise
