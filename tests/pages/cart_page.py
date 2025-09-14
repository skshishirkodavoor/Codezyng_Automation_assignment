
from selenium.webdriver.common.by import By
from loguru import logger

from tests.pages.base_page import BasePage


class CartPage(BasePage):
    """Shopping cart page class"""
    
    # Cart table
    CART_TABLE = (By.CSS_SELECTOR, ".table-responsive table")
    CART_ROWS = (By.CSS_SELECTOR, ".table-responsive tbody tr")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "td.text-left a")
    PRODUCT_QUANTITIES = (By.CSS_SELECTOR, "input[type='text']")
    UPDATE_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Update']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-original-title='Remove']")
    
    # Cart totals
    SUBTOTAL = (By.CSS_SELECTOR, ".table-responsive tbody tr:last-child td:last-child")
    TOTAL = (By.CSS_SELECTOR, ".table-responsive tbody tr:last-child td:last-child")
    
    # Cart actions
    CONTINUE_SHOPPING_BUTTON = (By.LINK_TEXT, "Continue Shopping")
    CHECKOUT_BUTTON = (By.LINK_TEXT, "Checkout")
    USE_COUPON_BUTTON = (By.LINK_TEXT, "Use Coupon Code")
    USE_GIFT_CERTIFICATE_BUTTON = (By.LINK_TEXT, "Use Gift Certificate")
    ESTIMATE_SHIPPING_BUTTON = (By.LINK_TEXT, "Estimate Shipping & Taxes")
    
    # Coupon code
    COUPON_INPUT = (By.ID, "input-coupon")
    COUPON_APPLY_BUTTON = (By.ID, "button-coupon")
    COUPON_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    COUPON_ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    
    # Gift certificate
    GIFT_CERTIFICATE_INPUT = (By.ID, "input-voucher")
    GIFT_CERTIFICATE_APPLY_BUTTON = (By.ID, "button-voucher")
    GIFT_CERTIFICATE_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    GIFT_CERTIFICATE_ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    
    # Empty cart
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".text-center p")
    EMPTY_CART_CONTINUE_BUTTON = (By.LINK_TEXT, "Continue")
    
    # Quantity update
    QUANTITY_INPUTS = (By.CSS_SELECTOR, "input[name*='quantity']")
    UPDATE_QUANTITY_BUTTONS = (By.CSS_SELECTOR, "button[data-original-title='Update']")
    
    def __init__(self, driver, wait_utils, screenshot_utils):
        super().__init__(driver, wait_utils, screenshot_utils)
        self.page_url = "/index.php?route=checkout/cart"
    
    def navigate_to_cart(self):
        """Navigate to shopping cart page"""
        try:
            full_url = self.driver.current_url.split('/')[0] + '//' + self.driver.current_url.split('/')[2] + self.page_url
            self.driver.get(full_url)
            self.wait_utils.wait_for_page_load()
            logger.info("Navigated to shopping cart page")
        except Exception as e:
            logger.error(f"Failed to navigate to cart: {str(e)}")
            raise
    
    def get_cart_items(self):
        """Get list of cart items"""
        try:
            cart_rows = self.find_elements(self.CART_ROWS)
            items = []
            for row in cart_rows:
                try:
                    product_name = row.find_element(By.CSS_SELECTOR, "td.text-left a").text
                    quantity_input = row.find_element(By.CSS_SELECTOR, "input[type='text']")
                    quantity = quantity_input.get_attribute("value")
                    price = row.find_element(By.CSS_SELECTOR, "td.text-right").text
                    total = row.find_elements(By.CSS_SELECTOR, "td.text-right")[-1].text
                    
                    items.append({
                        'product_name': product_name,
                        'quantity': int(quantity),
                        'price': price,
                        'total': total
                    })
                except Exception as e:
                    logger.warning(f"Failed to parse cart row: {str(e)}")
                    continue
            
            logger.info(f"Found {len(items)} items in cart")
            return items
        except Exception as e:
            logger.error(f"Failed to get cart items: {str(e)}")
            return []
    
    def get_product_names(self):
        """Get list of product names in cart"""
        try:
            product_elements = self.find_elements(self.PRODUCT_NAMES)
            product_names = [element.text for element in product_elements]
            logger.info(f"Cart product names: {product_names}")
            return product_names
        except Exception as e:
            logger.error(f"Failed to get product names: {str(e)}")
            return []
    
    def update_quantity(self, product_index, new_quantity):
        """Update quantity of specific product"""
        try:
            quantity_inputs = self.find_elements(self.QUANTITY_INPUTS)
            if product_index < len(quantity_inputs):
                quantity_inputs[product_index].clear()
                quantity_inputs[product_index].send_keys(str(new_quantity))
                
                # Click update button
                update_buttons = self.find_elements(self.UPDATE_QUANTITY_BUTTONS)
                if product_index < len(update_buttons):
                    update_buttons[product_index].click()
                
                logger.info(f"Updated quantity for product {product_index} to {new_quantity}")
                return True
            else:
                logger.error(f"Product index {product_index} not found")
                return False
        except Exception as e:
            logger.error(f"Failed to update quantity: {str(e)}")
            return False
    
    def remove_product(self, product_index):
        """Remove from cart"""
        try:
            remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
            if product_index < len(remove_buttons):
                remove_buttons[product_index].click()
                logger.info(f"Removed product {product_index} from cart")
                return True
            else:
                logger.error(f"Product index {product_index} not found")
                return False
        except Exception as e:
            logger.error(f"Failed to remove product: {str(e)}")
            return False
    
    def clear_cart(self):
        """Remove everything from cart"""
        try:
            remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
            for i in range(len(remove_buttons)):
                remove_buttons[i].click()
                # Wait for page to update
                self.wait_utils.wait_for_page_load()
                # Refresh remove buttons list
                remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
            
            logger.info("Cleared all items from cart")
        except Exception as e:
            logger.error(f"Failed to clear cart: {str(e)}")
            raise
    
    def get_subtotal(self):
        """Get cart subbtotal"""
        try:
            subtotal_text = self.get_element_text(self.SUBTOTAL)
            import re
            subtotal_match = re.search(r'[\d,]+\.?\d*', subtotal_text.replace(',', ''))
            if subtotal_match:
                subtotal = float(subtotal_match.group())
                logger.info(f"Cart subtotal: {subtotal}")
                return subtotal
            return 0.0
        except Exception as e:
            logger.error(f"Failed to get subtotal: {str(e)}")
            return 0.0
    
    def get_total(self):
        """Get cart total"""
        try:
            total_text = self.get_element_text(self.TOTAL)
            # Extract numeric value
            import re
            total_match = re.search(r'[\d,]+\.?\d*', total_text.replace(',', ''))
            if total_match:
                total = float(total_match.group())
                logger.info(f"Cart total: {total}")
                return total
            return 0.0
        except Exception as e:
            logger.error(f"Failed to get total: {str(e)}")
            return 0.0
    
    def click_continue_shopping(self):
        """Click continue shoping btn"""
        try:
            self.click_element(self.CONTINUE_SHOPPING_BUTTON)
            logger.info("Clicked continue shoping button")
        except Exception as e:
            logger.error(f"Failed to click continue shoping: {str(e)}")
            raise
    
    def click_checkout(self):
        """Click checkout bttn"""
        try:
            self.click_element(self.CHECKOUT_BUTTON)
            logger.info("Clicked checkout button")
        except Exception as e:
            logger.error(f"Failed to click checkout: {str(e)}")
            raise
    
    def apply_coupon_code(self, coupon_code):
        """Apply coupon"""
        try:
            self.click_element(self.USE_COUPON_BUTTON)
            self.send_keys_to_element(self.COUPON_INPUT, coupon_code)
            self.click_element(self.COUPON_APPLY_BUTTON)
            logger.info(f"applied coupon code: {coupon_code}")
        except Exception as e:
            logger.error(f"Failed to apply coupon code: {str(e)}")
            raise
    
    def get_coupon_success_message(self):
        """coupon success mssg"""
        try:
            if self.is_element_displayed(self.COUPON_SUCCESS_MESSAGE):
                message = self.get_element_text(self.COUPON_SUCCESS_MESSAGE)
                logger.info(f"Coupon success mssg: {message}")
                return message
            return None
        except Exception as e:
            logger.error(f"Failed to get coupon success mssg: {str(e)}")
            return None
    
    def get_coupon_error_message(self):
        """coupon error mssg"""
        try:
            if self.is_element_displayed(self.COUPON_ERROR_MESSAGE):
                message = self.get_element_text(self.COUPON_ERROR_MESSAGE)
                logger.info(f"Coupon error mssg: {message}")
                return message
            return None
        except Exception as e:
            logger.error(f"failed to get coupon error message: {str(e)}")
            return None
    
    def apply_gift_certificate(self, gift_certificate_code):
        """gift certificate"""
        try:
            self.click_element(self.USE_GIFT_CERTIFICATE_BUTTON)
            self.send_keys_to_element(self.GIFT_CERTIFICATE_INPUT, gift_certificate_code)
            self.click_element(self.GIFT_CERTIFICATE_APPLY_BUTTON)
            logger.info(f"gift certificate: {gift_certificate_code}")
        except Exception as e:
            logger.error(f"Failed gift certificate: {str(e)}")
            raise
    
    def get_gift_certificate_success_message(self):
        """gift certificate success msg"""
        try:
            if self.is_element_displayed(self.GIFT_CERTIFICATE_SUCCESS_MESSAGE):
                message = self.get_element_text(self.GIFT_CERTIFICATE_SUCCESS_MESSAGE)
                logger.info(f"Gift certificate success msg: {message}")
                return message
            return None
        except Exception as e:
            logger.error(f"Failed gift certificate msg: {str(e)}")
            return None
    
    def get_gift_certificate_error_message(self):
        """Get gift certificate error message"""
        try:
            if self.is_element_displayed(self.GIFT_CERTIFICATE_ERROR_MESSAGE):
                message = self.get_element_text(self.GIFT_CERTIFICATE_ERROR_MESSAGE)
                logger.info(f"Gift certificate error message: {message}")
                return message
            return None
        except Exception as e:
            logger.error(f"Failed to get gift certificate error message: {str(e)}")
            return None
    
    def is_cart_empty(self):
        """Check cart is empty"""
        try:
            return self.is_element_displayed(self.EMPTY_CART_MESSAGE)
        except Exception:
            return False
    
    def get_empty_cart_message(self):
        """Get empty cart message"""
        try:
            if self.is_cart_empty():
                message = self.get_element_text(self.EMPTY_CART_MESSAGE)
                logger.info(f"Empty cart message: {message}")
                return message
            return None
        except Exception as e:
            logger.error(f"Failed to get empty cart message: {str(e)}")
            return None
    
    def click_empty_cart_continue(self):
        """Click continue button when cart is empty"""
        try:
            self.click_element(self.EMPTY_CART_CONTINUE_BUTTON)
            logger.info("Clicked empty cart continue buttn")
        except Exception as e:
            logger.error(f"Failed to click empty cart continue: {str(e)}")
            raise
    
    def get_cart_items_count(self):
        """Get no. of items in cart"""
        try:
            items = self.get_cart_items()
            total_quantity = sum(item['quantity'] for item in items)
            logger.info(f"Cart item count: {total_quantity}")
            return total_quantity
        except Exception as e:
            logger.error(f"Failed to get cart item count: {str(e)}")
            return 0
