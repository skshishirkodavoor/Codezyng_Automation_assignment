from selenium.webdriver.common.by import By
from loguru import logger

from tests.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Checkout page class"""
    
    # Billing details
    FIRST_NAME_INPUT = (By.ID, "input-payment-firstname")
    LAST_NAME_INPUT = (By.ID, "input-payment-lastname")
    COMPANY_INPUT = (By.ID, "input-payment-company")
    ADDRESS_1_INPUT = (By.ID, "input-payment-address-1")
    ADDRESS_2_INPUT = (By.ID, "input-payment-address-2")
    CITY_INPUT = (By.ID, "input-payment-city")
    POSTCODE_INPUT = (By.ID, "input-payment-postcode")
    COUNTRY_SELECT = (By.ID, "input-payment-country")
    REGION_SELECT = (By.ID, "input-payment-zone")
    
    # Account details
    EMAIL_INPUT = (By.ID, "input-payment-email")
    TELEPHONE_INPUT = (By.ID, "input-payment-telephone")
    
    # Delivery details (same as billing)
    DELIVERY_FIRST_NAME_INPUT = (By.ID, "input-shipping-firstname")
    DELIVERY_LAST_NAME_INPUT = (By.ID, "input-shipping-lastname")
    DELIVERY_COMPANY_INPUT = (By.ID, "input-shipping-company")
    DELIVERY_ADDRESS_1_INPUT = (By.ID, "input-shipping-address-1")
    DELIVERY_ADDRESS_2_INPUT = (By.ID, "input-shipping-address-2")
    DELIVERY_CITY_INPUT = (By.ID, "input-shipping-city")
    DELIVERY_POSTCODE_INPUT = (By.ID, "input-shipping-postcode")
    DELIVERY_COUNTRY_SELECT = (By.ID, "input-shipping-country")
    DELIVERY_REGION_SELECT = (By.ID, "input-shipping-zone")
    
    # Checkboxes
    SAME_AS_BILLING_CHECKBOX = (By.NAME, "shipping_address")
    TERMS_CONDITIONS_CHECKBOX = (By.NAME, "agree")
    PRIVACY_POLICY_CHECKBOX = (By.NAME, "agree2")
    NEWSLETTER_CHECKBOX = (By.NAME, "newsletter")
    
    # Payment method
    PAYMENT_METHOD_RADIO = (By.CSS_SELECTOR, "input[name='payment_method']")
    CASH_ON_DELIVERY_RADIO = (By.CSS_SELECTOR, "input[value='cod']")
    BANK_TRANSFER_RADIO = (By.CSS_SELECTOR, "input[value='bank_transfer']")
    CHEQUE_RADIO = (By.CSS_SELECTOR, "input[value='cheque']")
    
    # Shipping method
    SHIPPING_METHOD_RADIO = (By.CSS_SELECTOR, "input[name='shipping_method']")
    FLAT_RATE_RADIO = (By.CSS_SELECTOR, "input[value='flat.flat']")
    
    # Buttons
    CONTINUE_BUTTON = (By.ID, "button-payment-address")
    CONTINUE_SHIPPING_BUTTON = (By.ID, "button-shipping-address")
    CONTINUE_SHIPPING_METHOD_BUTTON = (By.ID, "button-shipping-method")
    CONTINUE_PAYMENT_METHOD_BUTTON = (By.ID, "button-payment-method")
    CONFIRM_ORDER_BUTTON = (By.ID, "button-confirm")
    
    # Order summary
    ORDER_SUMMARY = (By.CSS_SELECTOR, ".table-responsive")
    ORDER_TOTAL = (By.CSS_SELECTOR, ".table-responsive tbody tr:last-child td:last-child")
    ORDER_CONFIRMATION = (By.CSS_SELECTOR, ".page-title")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".page-title")
    
    # Error messages
    ERROR_MESSAGES = (By.CSS_SELECTOR, ".text-danger")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    def __init__(self, driver, wait_utils, screenshot_utils):
        super().__init__(driver, wait_utils, screenshot_utils)
        self.page_url = "/index.php?route=checkout/checkout"
    
    def navigate_to_checkout(self):
        """Navigate chqout page"""
        try:
            full_url = self.driver.current_url.split('/')[0] + '//' + self.driver.current_url.split('/')[2] + self.page_url
            self.driver.get(full_url)
            self.wait_utils.wait_for_page_load()
            logger.info("Navigated to chqout page")
        except Exception as e:
            logger.error(f"Failed to navigate to cheqout: {str(e)}")
            raise
    
    def fill_billing_details(self, billing_data):
        """Fill billingform"""
        try:
            self.send_keys_to_element(self.FIRST_NAME_INPUT, billing_data.get('first_name', ''))
            self.send_keys_to_element(self.LAST_NAME_INPUT, billing_data.get('last_name', ''))
            self.send_keys_to_element(self.COMPANY_INPUT, billing_data.get('company', ''))
            self.send_keys_to_element(self.ADDRESS_1_INPUT, billing_data.get('address_1', ''))
            self.send_keys_to_element(self.ADDRESS_2_INPUT, billing_data.get('address_2', ''))
            self.send_keys_to_element(self.CITY_INPUT, billing_data.get('city', ''))
            self.send_keys_to_element(self.POSTCODE_INPUT, billing_data.get('postcode', ''))
            
            # Select country
            if billing_data.get('country'):
                self.select_dropdown_option(self.COUNTRY_SELECT, billing_data['country'])
            
            # Select region
            if billing_data.get('region'):
                self.select_dropdown_option(self.REGION_SELECT, billing_data['region'])
            
            logger.info("FilleD billing details")
        except Exception as e:
            logger.error(f"Failed to fill billing details: {str(e)}")
            raise
    
    def fill_account_details(self, account_data):
        """Fill account details form"""
        try:
            self.send_keys_to_element(self.EMAIL_INPUT, account_data.get('email', ''))
            self.send_keys_to_element(self.TELEPHONE_INPUT, account_data.get('telephone', ''))
            logger.info("Filled account details")
        except Exception as e:
            logger.error(f"Failed to fill account details: {str(e)}")
            raise
    
    def fill_delivery_details(self, delivery_data):
        """Fill delivery details form"""
        try:
            self.send_keys_to_element(self.DELIVERY_FIRST_NAME_INPUT, delivery_data.get('first_name', ''))
            self.send_keys_to_element(self.DELIVERY_LAST_NAME_INPUT, delivery_data.get('last_name', ''))
            self.send_keys_to_element(self.DELIVERY_COMPANY_INPUT, delivery_data.get('company', ''))
            self.send_keys_to_element(self.DELIVERY_ADDRESS_1_INPUT, delivery_data.get('address_1', ''))
            self.send_keys_to_element(self.DELIVERY_ADDRESS_2_INPUT, delivery_data.get('address_2', ''))
            self.send_keys_to_element(self.DELIVERY_CITY_INPUT, delivery_data.get('city', ''))
            self.send_keys_to_element(self.DELIVERY_POSTCODE_INPUT, delivery_data.get('postcode', ''))
            
            # Select country
            if delivery_data.get('country'):
                self.select_dropdown_option(self.DELIVERY_COUNTRY_SELECT, delivery_data['country'])
            
            # Select region
            if delivery_data.get('region'):
                self.select_dropdown_option(self.DELIVERY_REGION_SELECT, delivery_data['region'])
            
            logger.info("Filled delivery details")
        except Exception as e:
            logger.error(f"Failed to fill delivery details: {str(e)}")
            raise
    
    def check_same_as_billing(self):
        """Check same as billing address checkbox"""
        try:
            if not self.is_element_selected(self.SAME_AS_BILLING_CHECKBOX):
                self.click_element(self.SAME_AS_BILLING_CHECKBOX)
            logger.info("Checked same as billing address")
        except Exception as e:
            logger.error(f"Failed to check same as billing: {str(e)}")
            raise
    
    def uncheck_same_as_billing(self):
        """Uncheck same as billing address checkbox"""
        try:
            if self.is_element_selected(self.SAME_AS_BILLING_CHECKBOX):
                self.click_element(self.SAME_AS_BILLING_CHECKBOX)
            logger.info("Unchecked same as billing address")
        except Exception as e:
            logger.error(f"Failed to uncheck same as billing: {str(e)}")
            raise
    
    def select_payment_method(self, payment_method="cod"):
        """Select payment method"""
        try:
            if payment_method == "cod":
                self.click_element(self.CASH_ON_DELIVERY_RADIO)
            elif payment_method == "bank_transfer":
                self.click_element(self.BANK_TRANSFER_RADIO)
            elif payment_method == "cheque":
                self.click_element(self.CHEQUE_RADIO)
            else:
                # Select first available payment method
                payment_radios = self.find_elements(self.PAYMENT_METHOD_RADIO)
                if payment_radios:
                    payment_radios[0].click()
            
            logger.info(f"Selected payment method: {payment_method}")
        except Exception as e:
            logger.error(f"Failed to select payment method: {str(e)}")
            raise
    
    def select_shipping_method(self, shipping_method="flat.flat"):
        """Select shipping method"""
        try:
            if shipping_method == "flat.flat":
                self.click_element(self.FLAT_RATE_RADIO)
            else:
                # Select first available shipping method
                shipping_radios = self.find_elements(self.SHIPPING_METHOD_RADIO)
                if shipping_radios:
                    shipping_radios[0].click()
            
            logger.info(f"Selected shipping method: {shipping_method}")
        except Exception as e:
            logger.error(f"Failed to select shipping method: {str(e)}")
            raise
    
    def accept_terms_and_conditions(self):
        """Accept terms and conditions"""
        try:
            if not self.is_element_selected(self.TERMS_CONDITIONS_CHECKBOX):
                self.click_element(self.TERMS_CONDITIONS_CHECKBOX)
            logger.info("Accepted terms and conditions")
        except Exception as e:
            logger.error(f"Failed to accept terms and conditions: {str(e)}")
            raise
    
    def accept_privacy_policy(self):
        """Accept privacy policy"""
        try:
            if not self.is_element_selected(self.PRIVACY_POLICY_CHECKBOX):
                self.click_element(self.PRIVACY_POLICY_CHECKBOX)
            logger.info("Accepted privacy policy")
        except Exception as e:
            logger.error(f"Failed to accept privacy policy: {str(e)}")
            raise
    
    def subscribe_to_newsletter(self):
        """Subscribe to newsletter"""
        try:
            if not self.is_element_selected(self.NEWSLETTER_CHECKBOX):
                self.click_element(self.NEWSLETTER_CHECKBOX)
            logger.info("Subscribed to newsletter")
        except Exception as e:
            logger.error(f"Failed to subscribe to newsletter: {str(e)}")
            raise
    
    def click_continue(self):
        """Click continue button"""
        try:
            self.click_element(self.CONTINUE_BUTTON)
            logger.info("Clicked continue button")
        except Exception as e:
            logger.error(f"Failed to click continue: {str(e)}")
            raise
    
    def click_continue_shipping(self):
        """Click continue shipping button"""
        try:
            self.click_element(self.CONTINUE_SHIPPING_BUTTON)
            logger.info("Clicked continue shipping button")
        except Exception as e:
            logger.error(f"Failed to click continue shipping: {str(e)}")
            raise
    
    def click_continue_shipping_method(self):
        """Click continue shipping method button"""
        try:
            self.click_element(self.CONTINUE_SHIPPING_METHOD_BUTTON)
            logger.info("Clicked continue shipping method button")
        except Exception as e:
            logger.error(f"Failed to click continue shipping method: {str(e)}")
            raise
    
    def click_continue_payment_method(self):
        """Click continue payment method button"""
        try:
            self.click_element(self.CONTINUE_PAYMENT_METHOD_BUTTON)
            logger.info("Clicked continue payment method button")
        except Exception as e:
            logger.error(f"Failed to click continue payment method: {str(e)}")
            raise
    
    def confirm_order(self):
        """Confirm order"""
        try:
            self.click_element(self.CONFIRM_ORDER_BUTTON)
            logger.info("Confirmed order")
        except Exception as e:
            logger.error(f"Failed to confirm order: {str(e)}")
            raise
    
    def get_order_total(self):
        """Get order total"""
        try:
            total_text = self.get_element_text(self.ORDER_TOTAL)
            # Extract numeric value
            import re
            total_match = re.search(r'[\d,]+\.?\d*', total_text.replace(',', ''))
            if total_match:
                total = float(total_match.group())
                logger.info(f"Order total: {total}")
                return total
            return 0.0
        except Exception as e:
            logger.error(f"Failed to get order total: {str(e)}")
            return 0.0
    
    def get_order_confirmation(self):
        """Get order confirmation message"""
        try:
            if self.is_element_displayed(self.ORDER_CONFIRMATION):
                confirmation = self.get_element_text(self.ORDER_CONFIRMATION)
                logger.info(f"Order confirmation: {confirmation}")
                return confirmation
            return None
        except Exception as e:
            logger.error(f"Failed to get order confirmation: {str(e)}")
            return None
    
    def get_error_messages(self):
        """Get all error messages"""
        try:
            error_elements = self.find_elements(self.ERROR_MESSAGES)
            error_messages = [element.text for element in error_elements if element.text]
            logger.info(f"Error messages: {error_messages}")
            return error_messages
        except Exception as e:
            logger.error(f"Failed to get error messages: {str(e)}")
            return []
    
    def get_success_message(self):
        """Get success message"""
        try:
            if self.is_element_displayed(self.SUCCESS_MESSAGE):
                message = self.get_element_text(self.SUCCESS_MESSAGE)
                logger.info(f"Success message: {message}")
                return message
            return None
        except Exception as e:
            logger.error(f"Failed to get success message: {str(e)}")
            return None
    
    def complete_checkout(self, billing_data, account_data, payment_method="cod"):
        """Complete entire checkout process"""
        try:
            # Fill billing details
            self.fill_billing_details(billing_data)
            
            # Fill account details
            self.fill_account_details(account_data)
            
            # Click continue
            self.click_continue()
            
            # Wait for shipping section
            self.wait_utils.wait_for_page_load()
            
            # Check same as billing if delivery data not provided
            self.check_same_as_billing()
            
            # Click continue shipping
            self.click_continue_shipping()
            
            # Wait for shipping method section
            self.wait_utils.wait_for_page_load()
            
            # Select shipping method
            self.select_shipping_method()
            
            # Click continue shipping method
            self.click_continue_shipping_method()
            
            # Wait for payment method section
            self.wait_utils.wait_for_page_load()
            
            # Select payment method
            self.select_payment_method(payment_method)
            
            # Accept terms and conditions
            self.accept_terms_and_conditions()
            self.accept_privacy_policy()
            
            # Click continue payment method
            self.click_continue_payment_method()
            
            # Wait for confirm order section
            self.wait_utils.wait_for_page_load()
            
            # Confirm order
            self.confirm_order()
            
            logger.info("Checkout process completed successfully")
            
        except Exception as e:
            logger.error(f"Checkout process failed: {str(e)}")
            raise
