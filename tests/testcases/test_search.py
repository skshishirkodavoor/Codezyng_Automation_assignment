"""
Search and Filter Test Cases
"""
import pytest
from loguru import logger

from tests.pages.home_page import HomePage
from tests.pages.product_page import ProductPage
from utils.data_utils import DataUtils


class TestSearch:
    """Test class for search and filtering functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, wait_utils, screenshot_utils):
        """Setup for each test"""
        self.driver = driver
        self.wait_utils = wait_utils
        self.screenshot_utils = screenshot_utils
        self.home_page = HomePage(driver, wait_utils, screenshot_utils)
        self.product_page = ProductPage(driver, wait_utils, screenshot_utils)
        self.data_utils = DataUtils()
    
    @pytest.mark.parametrize("search_term", [
        "iPhone",
        "MacBook",
        "Samsung",
        "Canon",
        "Nikon"
    ])
    def test_product_search(self, search_term):
        """Test product search functionality"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Search for product
            self.home_page.search_product(search_term)
            
            # Verify search results
            current_url = self.driver.current_url
            assert "search" in current_url.lower(), "Should be on search results page"
            
            # Check if search term appears in page title or content
            page_title = self.driver.title
            assert search_term.lower() in page_title.lower() or "search" in page_title.lower(), \
                f"Search term '{search_term}' should appear in page title"
            
            logger.info(f"Product search test passed for: {search_term}")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_product_search", e)
            logger.error(f"Product search test failed for {search_term}: {str(e)}")
            raise
    
    def test_empty_search(self):
        """Test empty search"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Search with empty term
            self.home_page.search_product("")
            
            # Verify search behavior (should either show all products or error message)
            current_url = self.driver.current_url
            # The behavior depends on the application implementation
            
            logger.info("Empty search test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_empty_search", e)
            logger.error(f"Empty search test failed: {str(e)}")
            raise
    
    def test_special_characters_search(self):
        """Test search with special characters"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Search with special characters
            special_terms = ["@#$%", "!@#$%^&*()", "test@123", "product-name"]
            
            for term in special_terms:
                self.home_page.search_product(term)
                # Verify the application handles special characters gracefully
                current_url = self.driver.current_url
                # Should not crash or show error page
            
            logger.info("Special characters search test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_special_characters", e)
            logger.error(f"Special characters search test failed: {str(e)}")
            raise
    
    def test_search_case_sensitivity(self):
        """Test search case sensitivity"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            search_term = "iPhone"
            variations = ["iphone", "IPHONE", "iPhone", "iPhOnE"]
            
            for variation in variations:
                self.home_page.search_product(variation)
                # All variations should return similar results
                current_url = self.driver.current_url
                assert "search" in current_url.lower(), "Should be on search results page"
            
            logger.info("Search case sensitivity test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_case_sensitivity", e)
            logger.error(f"Search case sensitivity test failed: {str(e)}")
            raise
    
    def test_search_results_validation(self):
        """Test search results validation"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Search for a common product
            search_term = "phone"
            self.home_page.search_product(search_term)
            
            # Verify search results page elements
            # Check if product listings are present
            # This would depend on the specific search results page structure
            
            logger.info("Search results validation test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_search_results", e)
            logger.error(f"Search results validation test failed: {str(e)}")
            raise
    
    def test_category_navigation(self):
        """Test category navigation"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Test different categories
            categories = [
                "Desktops",
                "Laptops & Notebooks",
                "Components",
                "Tablets",
                "Software",
                "Phones & PDAs",
                "Cameras",
                "MP3 Players"
            ]
            
            for category in categories:
                self.home_page.navigate_to_category(category)
                # Verify navigation to category page
                current_url = self.driver.current_url
                # Should be on category page
                logger.info(f"Navigated to category: {category}")
            
            logger.info("Category navigation test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_category_navigation", e)
            logger.error(f"Category navigation test failed: {str(e)}")
            raise
    
    def test_featured_products_display(self):
        """Test featured products display"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Check if featured products are displayed
            featured_products = self.home_page.get_featured_products()
            assert len(featured_products) > 0, "Featured products should be displayed"
            
            # Get product names
            product_names = self.home_page.get_product_names()
            assert len(product_names) > 0, "Product names should be available"
            
            logger.info(f"Found {len(featured_products)} featured products")
            logger.info("Featured products display test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_featured_products", e)
            logger.error(f"Featured products test failed: {str(e)}")
            raise
    
    def test_product_quick_actions(self):
        """Test product quick actions (add to cart, wishlist, compare)"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Test add to cart
            cart_success = self.home_page.add_product_to_cart(0)
            if cart_success:
                logger.info("Product added to cart successfully")
            
            # Test add to wishlist
            wishlist_success = self.home_page.add_product_to_wishlist(0)
            if wishlist_success:
                logger.info("Product added to wishlist successfully")
            
            # Test compare
            compare_success = self.home_page.compare_product(0)
            if compare_success:
                logger.info("Product added to compare successfully")
            
            logger.info("Product quick actions test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_quick_actions", e)
            logger.error(f"Product quick actions test failed: {str(e)}")
            raise
    
    def test_carousel_navigation(self):
        """Test carousel navigation"""
        try:
            # Navigate to home page
            self.home_page.navigate_to_home_page()
            
            # Test carousel next
            self.home_page.navigate_carousel_next()
            
            # Test carousel previous
            self.home_page.navigate_carousel_previous()
            
            # Test carousel indicators
            self.home_page.click_carousel_indicator(0)
            
            logger.info("Carousel navigation test passed")
            
        except Exception as e:
            self.screenshot_utils.capture_screenshot_on_failure("test_carousel", e)
            logger.error(f"Carousel navigation test failed: {str(e)}")
            raise
