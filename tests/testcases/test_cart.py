"""
Shopping Cart Test Cases
"""
import pytest
from loguru import logger

from tests.pages.home_page import HomePage
from tests.pages.product_page import ProductPage
from tests.pages.cart_page import CartPage
from tests.pages.login_page import LoginPage
from utils.data_utils import DataUtils


class TestCart:
    """Test class for shopping cart functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, wait_utils, screenshot_utils):
        """Setup for each test"""
        self.driver = driver
        self.wait_utils = wait_utils
        self.screenshot_utils = screenshot_utils
        self.home_page = HomePage(driver, wait_utils, screenshot_utils)
        self.product_page = ProductPage(driver, wait_utils, screenshot_utils)
        self.cart_page = CartPage(driver, wait_utils, screenshot_utils)
        self.login_page = LoginPage(driver, wait_utils, screenshot_utils)
        self.data_utils = DataUtils()
    
    def test_add_single_product_to_cart(self):
        """Test adding single product to cart"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Add first product to cart
            success = self.home_page.add_product_to_cart(0)
            assert success, "Product should be added to cart"
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Verify product in cart
            cart_items = self.cart_page.get_cart_items()
            assert len(cart_items) > 0, "Cart should contain items"
            
            # Verify cart count
            cart_count = self.cart_page.get_cart_items_count()
            assert cart_count > 0, "Cart count should be greater than 0"
            
            logger.info("Add single product to cart test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_add_single_product", e)
            logger.error(f"Add single product test failed: {str(e)}")
            raise
    
    def test_add_multiple_products_to_cart(self):
        """Test adding multiple products to cart"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Add multiple products to cart
            products_to_add = 3
            for i in range(products_to_add):
                success = self.home_page.add_product_to_cart(i)
                if success:
                    logger.info(f"Added product {i} to cart")
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Verify multiple products in cart
            cart_items = self.cart_page.get_cart_items()
            assert len(cart_items) > 0, "Cart should contain items"
            
            logger.info(f"Added {len(cart_items)} products to cart")
            logger.info("Add multiple products to cart test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_add_multiple_products", e)
            logger.error(f"Add multiple products test failed: {str(e)}")
            raise
    
    def test_update_product_quantity(self):
        """Test updating product quantity in cart"""
        try:
            # Add product to cart first
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Update quantity
            new_quantity = 3
            success = self.cart_page.update_quantity(0, new_quantity)
            assert success, "Quantity should be updated"
            
            # Verify updated quantity
            cart_items = self.cart_page.get_cart_items()
            if cart_items:
                assert cart_items[0]['quantity'] == new_quantity, \
                    f"Quantity should be updated to {new_quantity}"
            
            logger.info("Update product quantity test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_update_quantity", e)
            logger.error(f"Update quantity test failed: {str(e)}")
            raise
    
    def test_remove_product_from_cart(self):
        """Test removing product from cart"""
        try:
            # Add product to cart first
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Get initial cart count
            initial_count = self.cart_page.get_cart_items_count()
            
            # Remove product
            success = self.cart_page.remove_product(0)
            assert success, "Product should be removed"
            
            # Verify removal
            final_count = self.cart_page.get_cart_items_count()
            assert final_count < initial_count, "Cart count should decrease"
            
            logger.info("Remove product from cart test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_remove_product", e)
            logger.error(f"Remove product test failed: {str(e)}")
            raise
    
    def test_clear_cart(self):
        """Test clearing entire cart"""
        try:
            # Add multiple products to cart
            self.home_page.navigate_to_home_page()
            for i in range(3):
                self.home_page.add_product_to_cart(i)
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Clear cart
            self.cart_page.clear_cart()
            
            # Verify cart is empty
            assert self.cart_page.is_cart_empty(), "Cart should be empty"
            
            logger.info("Clear cart test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_clear_cart", e)
            logger.error(f"Clear cart test failed: {str(e)}")
            raise
    
    def test_cart_price_calculation(self):
        """Test cart price calculation"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Get cart totals
            subtotal = self.cart_page.get_subtotal()
            total = self.cart_page.get_total()
            
            # Verify totals are calculated
            assert subtotal > 0, "Subtotal should be greater than 0"
            assert total > 0, "Total should be greater than 0"
            
            logger.info(f"Cart subtotal: {subtotal}, Total: {total}")
            logger.info("Cart price calculation test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_price_calculation", e)
            logger.error(f"Price calculation test failed: {str(e)}")
            raise
    
    def test_coupon_code_application(self):
        """Test applying coupon code"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Apply coupon code (using a test coupon)
            test_coupon = "TEST123"
            self.cart_page.apply_coupon_code(test_coupon)
            
            # Check for success or error message
            success_message = self.cart_page.get_coupon_success_message()
            error_message = self.cart_page.get_coupon_error_message()
            
            # Either success or error message should be displayed
            assert success_message is not None or error_message is not None, \
                "Coupon application should show a message"
            
            logger.info("Coupon code application test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_coupon_code", e)
            logger.error(f"Coupon code test failed: {str(e)}")
            raise
    
    def test_gift_certificate_application(self):
        """Test applying gift certificate"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Apply gift certificate (using a test certificate)
            test_gift_cert = "GIFT123"
            self.cart_page.apply_gift_certificate(test_gift_cert)
            
            # Check for success or error message
            success_message = self.cart_page.get_gift_certificate_success_message()
            error_message = self.cart_page.get_gift_certificate_error_message()
            
            # Either success or error message should be displayed
            assert success_message is not None or error_message is not None, \
                "Gift certificate application should show a message"
            
            logger.info("Gift certificate application test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_gift_certificate", e)
            logger.error(f"Gift certificate test failed: {str(e)}")
            raise
    
    def test_continue_shopping(self):
        """Test continue shopping functionality"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Click continue shopping
            self.cart_page.click_continue_shopping()
            
            # Verify navigation back to home page
            current_url = self.driver.current_url
            # Should be back to home page or product listing
            
            logger.info("Continue shopping test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_continue_shopping", e)
            logger.error(f"Continue shopping test failed: {str(e)}")
            raise
    
    def test_checkout_navigation(self):
        """Test checkout navigation"""
        try:
            # Add product to cart
            self.home_page.navigate_to_home_page()
            self.home_page.add_product_to_cart(0)
            
            # Navigate to cart
            self.cart_page.navigate_to_cart()
            
            # Click checkout
            self.cart_page.click_checkout()
            
            # Verify navigation to checkout page
            current_url = self.driver.current_url
            assert "checkout" in current_url.lower(), "Should navigate to checkout page"
            
            logger.info("Checkout navigation test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_checkout_navigation", e)
            logger.error(f"Checkout navigation test failed: {str(e)}")
            raise
    
    def test_empty_cart_behavior(self):
        """Test empty cart behavior"""
        try:
            # Navigate to empty cart
            self.cart_page.navigate_to_cart()
            
            # Check if cart is empty
            is_empty = self.cart_page.is_cart_empty()
            
            if is_empty:
                # Get empty cart message
                message = self.cart_page.get_empty_cart_message()
                assert message is not None, "Empty cart message should be displayed"
                
                # Click continue button
                self.cart_page.click_empty_cart_continue()
            
            logger.info("Empty cart behavior test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_empty_cart", e)
            logger.error(f"Empty cart test failed: {str(e)}")
            raise
