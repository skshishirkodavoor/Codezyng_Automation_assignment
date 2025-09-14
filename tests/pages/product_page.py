"""
Product Page Object Model
"""
from selenium.webdriver.common.by import By
from loguru import logger

from tests.pages.base_page import BasePage


class ProductPage(BasePage):
    """Product page class"""
    
    # Product details
    PRODUCT_NAME = (By.CSS_SELECTOR, "h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".price-new, .price")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, "#tab-description")
    PRODUCT_SPECIFICATIONS = (By.CSS_SELECTOR, "#tab-specification")
    PRODUCT_REVIEWS = (By.CSS_SELECTOR, "#tab-review")
    
    # Product options
    QUANTITY_INPUT = (By.NAME, "quantity")
    ADD_TO_CART_BUTTON = (By.ID, "button-cart")
    ADD_TO_WISHLIST_BUTTON = (By.CSS_SELECTOR, "[data-original-title='Add to Wish List']")
    COMPARE_BUTTON = (By.CSS_SELECTOR, "[data-original-title='Compare this Product']")
    
    # Product images
    MAIN_IMAGE = (By.CSS_SELECTOR, ".thumbnails img")
    THUMBNAIL_IMAGES = (By.CSS_SELECTOR, ".thumbnails a")
    ZOOM_IMAGE = (By.CSS_SELECTOR, ".mfp-img")
    
    # Product tabs
    DESCRIPTION_TAB = (By.CSS_SELECTOR, "a[href='#tab-description']")
    SPECIFICATION_TAB = (By.CSS_SELECTOR, "a[href='#tab-specification']")
    REVIEWS_TAB = (By.CSS_SELECTOR, "a[href='#tab-review']")
    
    # Reviews section
    REVIEW_NAME_INPUT = (By.ID, "input-name")
    REVIEW_TEXT_INPUT = (By.ID, "input-review")
    REVIEW_RATING_RADIO = (By.CSS_SELECTOR, "input[name='rating']")
    REVIEW_SUBMIT_BUTTON = (By.ID, "button-review")
    REVIEW_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    REVIEW_ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    
    # Related products
    RELATED_PRODUCTS = (By.CSS_SELECTOR, ".product-layout")
    RELATED_PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-layout h4 a")
    
    # Breadcrumb
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb")
    BREADCRUMB_LINKS = (By.CSS_SELECTOR, ".breadcrumb a")
    
    def __init__(self, driver, wait_utils, screenshot_utils):
        super().__init__(driver, wait_utils, screenshot_utils)
    
    def get_product_name(self):
        """Get product name"""
        try:
            product_name = self.get_element_text(self.PRODUCT_NAME)
            logger.info(f"Product name: {product_name}")
            return product_name
        except Exception as e:
            logger.error(f"Failed to get product name: {str(e)}")
            return ""
    
    def get_product_price(self):
        """Get product price"""
        try:
            price_text = self.get_element_text(self.PRODUCT_PRICE)
            # Extract numeric value from price text
            import re
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
            if price_match:
                price = float(price_match.group())
                logger.info(f"Product price: {price}")
                return price
            return 0.0
        except Exception as e:
            logger.error(f"Failed to get product price: {str(e)}")
            return 0.0
    
    def get_product_description(self):
        """Get product description"""
        try:
            description = self.get_element_text(self.PRODUCT_DESCRIPTION)
            logger.info(f"Product description: {description[:100]}...")
            return description
        except Exception as e:
            logger.error(f"Failed to get product description: {str(e)}")
            return ""
    
    def set_quantity(self, quantity):
        """Set product quantity"""
        try:
            self.send_keys_to_element(self.QUANTITY_INPUT, str(quantity))
            logger.info(f"Set quantity to: {quantity}")
        except Exception as e:
            logger.error(f"Failed to set quantity: {str(e)}")
            raise
    
    def add_to_cart(self, quantity=1):
        """Add product to cart"""
        try:
            if quantity > 1:
                self.set_quantity(quantity)
            
            self.click_element(self.ADD_TO_CART_BUTTON)
            logger.info(f"Added {quantity} items to cart")
        except Exception as e:
            logger.error(f"Failed to add to cart: {str(e)}")
            raise
    
    def add_to_wishlist(self):
        """Add product to wishlist"""
        try:
            self.click_element(self.ADD_TO_WISHLIST_BUTTON)
            logger.info("Added product to wishlist")
        except Exception as e:
            logger.error(f"Failed to add to wishlist: {str(e)}")
            raise
    
    def add_to_compare(self):
        """Add product to compare"""
        try:
            self.click_element(self.COMPARE_BUTTON)
            logger.info("Added product to compare")
        except Exception as e:
            logger.error(f"Failed to add to compare: {str(e)}")
            raise
    
    def click_thumbnail_image(self, thumbnail_index=0):
        """Click thumbnail image"""
        try:
            thumbnails = self.find_elements(self.THUMBNAIL_IMAGES)
            if thumbnail_index < len(thumbnails):
                thumbnails[thumbnail_index].click()
                logger.info(f"Clicked thumbnail {thumbnail_index}")
            else:
                logger.error(f"Thumbnail {thumbnail_index} not found")
        except Exception as e:
            logger.error(f"Failed to click thumbnail: {str(e)}")
            raise
    
    def click_main_image(self):
        """Click main product image"""
        try:
            self.click_element(self.MAIN_IMAGE)
            logger.info("Clicked main product image")
        except Exception as e:
            logger.error(f"Failed to click main image: {str(e)}")
            raise
    
    def switch_to_description_tab(self):
        """Switch to description tab"""
        try:
            self.click_element(self.DESCRIPTION_TAB)
            logger.info("Switched to description tab")
        except Exception as e:
            logger.error(f"Failed to switch to description tab: {str(e)}")
            raise
    
    def switch_to_specification_tab(self):
        """Switch to specification tab"""
        try:
            self.click_element(self.SPECIFICATION_TAB)
            logger.info("Switched to specification tab")
        except Exception as e:
            logger.error(f"Failed to switch to specification tab: {str(e)}")
            raise
    
    def switch_to_reviews_tab(self):
        """Switch to reviews tab"""
        try:
            self.click_element(self.REVIEWS_TAB)
            logger.info("Switched to reviews tab")
        except Exception as e:
            logger.error(f"Failed to switch to reviews tab: {str(e)}")
            raise
    
    def write_review(self, name, review_text, rating=5):
        """Write a product review"""
        try:
            # Switch to reviews tab first
            self.switch_to_reviews_tab()
            
            # Fill review form
            self.send_keys_to_element(self.REVIEW_NAME_INPUT, name)
            self.send_keys_to_element(self.REVIEW_TEXT_INPUT, review_text)
            
            # Select rating
            rating_radios = self.find_elements(self.REVIEW_RATING_RADIO)
            if rating <= len(rating_radios):
                rating_radios[rating - 1].click()
            
            # Submit review
            self.click_element(self.REVIEW_SUBMIT_BUTTON)
            logger.info(f"Submitted review with rating {rating}")
        except Exception as e:
            logger.error(f"Failed to write review: {str(e)}")
            raise
    
    def get_review_success_message(self):
        """Get review success message"""
        try:
            if self.is_element_displayed(self.REVIEW_SUCCESS_MESSAGE):
                message = self.get_element_text(self.REVIEW_SUCCESS_MESSAGE)
                logger.info(f"Review success message: {message}")
                return message
            return None
        except Exception as e:
            logger.error(f"Failed to get review success message: {str(e)}")
            return None
    
    def get_review_error_message(self):
        """Get review error message"""
        try:
            if self.is_element_displayed(self.REVIEW_ERROR_MESSAGE):
                message = self.get_element_text(self.REVIEW_ERROR_MESSAGE)
                logger.info(f"Review error message: {message}")
                return message
            return None
        except Exception as e:
            logger.error(f"Failed to get review error message: {str(e)}")
            return None
    
    def get_related_products(self):
        """Get list of related products"""
        try:
            related_products = self.find_elements(self.RELATED_PRODUCTS)
            logger.info(f"Found {len(related_products)} related products")
            return related_products
        except Exception as e:
            logger.error(f"Failed to get related products: {str(e)}")
            return []
    
    def get_related_product_names(self):
        """Get names of related products"""
        try:
            product_elements = self.find_elements(self.RELATED_PRODUCT_NAMES)
            product_names = [element.text for element in product_elements]
            logger.info(f"Related product names: {product_names}")
            return product_names
        except Exception as e:
            logger.error(f"Failed to get related product names: {str(e)}")
            return []
    
    def click_related_product(self, product_index=0):
        """Click on related product by index"""
        try:
            related_products = self.find_elements(self.RELATED_PRODUCT_NAMES)
            if product_index < len(related_products):
                related_products[product_index].click()
                logger.info(f"Clicked related product {product_index}")
            else:
                logger.error(f"Related product {product_index} not found")
        except Exception as e:
            logger.error(f"Failed to click related product: {str(e)}")
            raise
    
    def get_breadcrumb_links(self):
        """Get breadcrumb navigation links"""
        try:
            breadcrumb_links = self.find_elements(self.BREADCRUMB_LINKS)
            link_texts = [link.text for link in breadcrumb_links]
            logger.info(f"Breadcrumb links: {link_texts}")
            return link_texts
        except Exception as e:
            logger.error(f"Failed to get breadcrumb links: {str(e)}")
            return []
    
    def click_breadcrumb_link(self, link_text):
        """Click breadcrumb link by text"""
        try:
            breadcrumb_links = self.find_elements(self.BREADCRUMB_LINKS)
            for link in breadcrumb_links:
                if link.text == link_text:
                    link.click()
                    logger.info(f"Clicked breadcrumb link: {link_text}")
                    return
            logger.error(f"Breadcrumb link '{link_text}' not found")
        except Exception as e:
            logger.error(f"Failed to click breadcrumb link: {str(e)}")
            raise
