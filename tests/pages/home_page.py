"""
Home Page Object Model
"""
from selenium.webdriver.common.by import By
from loguru import logger

from tests.pages.base_page import BasePage


class HomePage(BasePage):
    """Home page class"""
    
    # Locators
    LOGO = (By.CSS_SELECTOR, "#logo")
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".btn-default")
    CART_BUTTON = (By.CSS_SELECTOR, "#cart")
    CART_ITEMS_COUNT = (By.CSS_SELECTOR, "#cart .badge")
    ACCOUNT_DROPDOWN = (By.CSS_SELECTOR, ".dropdown .dropdown-toggle")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    WISHLIST_LINK = (By.LINK_TEXT, "Wish List")
    SHOPPING_CART_LINK = (By.LINK_TEXT, "Shopping Cart")
    CHECKOUT_LINK = (By.LINK_TEXT, "Checkout")
    
    # Navigation menu
    DESKTOPS_MENU = (By.LINK_TEXT, "Desktops")
    LAPTOPS_MENU = (By.LINK_TEXT, "Laptops & Notebooks")
    COMPONENTS_MENU = (By.LINK_TEXT, "Components")
    TABLETS_MENU = (By.LINK_TEXT, "Tablets")
    SOFTWARE_MENU = (By.LINK_TEXT, "Software")
    PHONES_MENU = (By.LINK_TEXT, "Phones & PDAs")
    CAMERAS_MENU = (By.LINK_TEXT, "Cameras")
    MP3_MENU = (By.LINK_TEXT, "MP3 Players")
    
    # Featured products
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".product-layout")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-layout h4 a")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".product-layout .button-group .btn-primary")
    ADD_TO_WISHLIST_BUTTONS = (By.CSS_SELECTOR, ".product-layout .button-group .btn-default")
    COMPARE_BUTTONS = (By.CSS_SELECTOR, ".product-layout .button-group .btn-default[data-original-title='Compare this Product']")
    
    # Carousel
    CAROUSEL_NEXT = (By.CSS_SELECTOR, ".carousel-control.right")
    CAROUSEL_PREV = (By.CSS_SELECTOR, ".carousel-control.left")
    CAROUSEL_INDICATORS = (By.CSS_SELECTOR, ".carousel-indicators li")
    
    def __init__(self, driver, wait_utils, screenshot_utils):
        super().__init__(driver, wait_utils, screenshot_utils)
        self.page_url = "/"
    
    def navigate_to_home_page(self):
        """Navigate to home page"""
        try:
            self.driver.get(self.driver.current_url.split('/')[0] + '//' + self.driver.current_url.split('/')[2] + self.page_url)
            self.wait_utils.wait_for_page_load()
            logger.info("Navigated to home page")
        except Exception as e:
            logger.error(f"Failed to navigate to home page: {str(e)}")
            raise
    
    def search_product(self, product_name):
        """Search for a product"""
        try:
            self.send_keys_to_element(self.SEARCH_INPUT, product_name)
            self.click_element(self.SEARCH_BUTTON)
            logger.info(f"Searched for product: {product_name}")
        except Exception as e:
            logger.error(f"Failed to search product: {str(e)}")
            raise
    
    def get_cart_items_count(self):
        """Get number of items in cart"""
        try:
            if self.is_element_displayed(self.CART_ITEMS_COUNT):
                count_text = self.get_element_text(self.CART_ITEMS_COUNT)
                return int(count_text) if count_text.isdigit() else 0
            return 0
        except Exception as e:
            logger.error(f"Failed to get cart items count: {str(e)}")
            return 0
    
    def click_cart_button(self):
        """Click cart button"""
        try:
            self.click_element(self.CART_BUTTON)
            logger.info("Clicked cart button")
        except Exception as e:
            logger.error(f"Failed to click cart button: {str(e)}")
            raise
    
    def click_login_link(self):
        """Click login link"""
        try:
            self.click_element(self.LOGIN_LINK)
            logger.info("Clicked login link")
        except Exception as e:
            logger.error(f"Failed to click login link: {str(e)}")
            raise
    
    def click_register_link(self):
        """Click register link"""
        try:
            self.click_element(self.REGISTER_LINK)
            logger.info("Clicked register link")
        except Exception as e:
            logger.error(f"Failed to click register link: {str(e)}")
            raise
    
    def click_wishlist_link(self):
        """Click wishlist link"""
        try:
            self.click_element(self.WISHLIST_LINK)
            logger.info("Clicked wishlist link")
        except Exception as e:
            logger.error(f"Failed to click wishlist link: {str(e)}")
            raise
    
    def click_shopping_cart_link(self):
        """Click shopping cart link"""
        try:
            self.click_element(self.SHOPPING_CART_LINK)
            logger.info("Clicked shopping cart link")
        except Exception as e:
            logger.error(f"Failed to click shopping cart link: {str(e)}")
            raise
    
    def click_checkout_link(self):
        """Click checkout link"""
        try:
            self.click_element(self.CHECKOUT_LINK)
            logger.info("Clicked checkout link")
        except Exception as e:
            logger.error(f"Failed to click checkout link: {str(e)}")
            raise
    
    def navigate_to_category(self, category_name):
        """Navigate to specific category"""
        try:
            category_locator = self._get_category_locator(category_name)
            self.click_element(category_locator)
            logger.info(f"Navigated to category: {category_name}")
        except Exception as e:
            logger.error(f"Failed to navigate to category {category_name}: {str(e)}")
            raise
    
    def _get_category_locator(self, category_name):
        """Get locator for specific category"""
        category_locators = {
            "Desktops": self.DESKTOPS_MENU,
            "Laptops & Notebooks": self.LAPTOPS_MENU,
            "Components": self.COMPONENTS_MENU,
            "Tablets": self.TABLETS_MENU,
            "Software": self.SOFTWARE_MENU,
            "Phones & PDAs": self.PHONES_MENU,
            "Cameras": self.CAMERAS_MENU,
            "MP3 Players": self.MP3_MENU
        }
        return category_locators.get(category_name, (By.LINK_TEXT, category_name))
    
    def get_featured_products(self):
        """Get list of featured products"""
        try:
            products = self.find_elements(self.FEATURED_PRODUCTS)
            logger.info(f"Found {len(products)} featured products")
            return products
        except Exception as e:
            logger.error(f"Failed to get featured products: {str(e)}")
            return []
    
    def get_product_names(self):
        """Get list of product names"""
        try:
            product_elements = self.find_elements(self.PRODUCT_NAMES)
            product_names = [element.text for element in product_elements]
            logger.info(f"Found product names: {product_names}")
            return product_names
        except Exception as e:
            logger.error(f"Failed to get product names: {str(e)}")
            return []
    
    def add_product_to_cart(self, product_index=0):
        """Add product to cart by index"""
        try:
            add_to_cart_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
            if product_index < len(add_to_cart_buttons):
                add_to_cart_buttons[product_index].click()
                logger.info(f"Added product {product_index} to cart")
                return True
            else:
                logger.error(f"Product index {product_index} not found")
                return False
        except Exception as e:
            logger.error(f"Failed to add product to cart: {str(e)}")
            return False
    
    def add_product_to_wishlist(self, product_index=0):
        """Add product to wishlist by index"""
        try:
            wishlist_buttons = self.find_elements(self.ADD_TO_WISHLIST_BUTTONS)
            if product_index < len(wishlist_buttons):
                wishlist_buttons[product_index].click()
                logger.info(f"Added product {product_index} to wishlist")
                return True
            else:
                logger.error(f"Product index {product_index} not found")
                return False
        except Exception as e:
            logger.error(f"Failed to add product to wishlist: {str(e)}")
            return False
    
    def compare_product(self, product_index=0):
        """Add product to compare by index"""
        try:
            compare_buttons = self.find_elements(self.COMPARE_BUTTONS)
            if product_index < len(compare_buttons):
                compare_buttons[product_index].click()
                logger.info(f"Added product {product_index} to compare")
                return True
            else:
                logger.error(f"Product index {product_index} not found")
                return False
        except Exception as e:
            logger.error(f"Failed to add product to compare: {str(e)}")
            return False
    
    def navigate_carousel_next(self):
        """Navigate carousel to next slide"""
        try:
            self.click_element(self.CAROUSEL_NEXT)
            logger.info("Navigated carousel to next slide")
        except Exception as e:
            logger.error(f"Failed to navigate carousel next: {str(e)}")
            raise
    
    def navigate_carousel_previous(self):
        """Navigate carousel to previous slide"""
        try:
            self.click_element(self.CAROUSEL_PREV)
            logger.info("Navigated carousel to previous slide")
        except Exception as e:
            logger.error(f"Failed to navigate carousel previous: {str(e)}")
            raise
    
    def click_carousel_indicator(self, indicator_index):
        """Click specific carousel indicator"""
        try:
            indicators = self.find_elements(self.CAROUSEL_INDICATORS)
            if indicator_index < len(indicators):
                indicators[indicator_index].click()
                logger.info(f"Clicked carousel indicator {indicator_index}")
            else:
                logger.error(f"Carousel indicator {indicator_index} not found")
        except Exception as e:
            logger.error(f"Failed to click carousel indicator: {str(e)}")
            raise
    
    def is_logo_displayed(self):
        """Check if logo is displayed"""
        try:
            return self.is_element_displayed(self.LOGO)
        except Exception:
            return False
    
    def get_page_title(self):
        """Get page title"""
        try:
            return self.driver.title
        except Exception as e:
            logger.error(f"Failed to get page title: {str(e)}")
            return ""
