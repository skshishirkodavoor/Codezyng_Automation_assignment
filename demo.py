"""
Demo script showing how to use the E-commerce Automation Framework
"""
import time
from utils.driver_manager import DriverManager
from utils.config_reader import ConfigReader
from utils.wait_utils import WaitUtils
from utils.screenshot_utils import ScreenshotUtils
from tests.pages.home_page import HomePage
from tests.pages.login_page import LoginPage


def demo_basic_usage():
    """Demonstrate basic framework usage"""
    print("🚀 E-commerce Automation Framework Demo")
    print("=" * 40)
    
    # Initialize configuration
    config = ConfigReader()
    print(f"📋 Base URL: {config.get_base_url()}")
    print(f"🌐 Browser: {config.get_browser()}")
    
    # Initialize driver
    driver_manager = DriverManager(
        browser=config.get_browser(),
        headless=config.get_headless()
    )
    
    try:
        # Get driver
        driver = driver_manager.get_driver()
        print("✅ Driver initialized successfully")
        
        # Initialize utilities
        wait_utils = WaitUtils(driver, config.get_explicit_wait())
        screenshot_utils = ScreenshotUtils(driver, config.get_screenshot_path())
        
        # Initialize page objects
        home_page = HomePage(driver, wait_utils, screenshot_utils)
        login_page = LoginPage(driver, wait_utils, screenshot_utils)
        
        # Navigate to home page
        print("🏠 Navigating to home page...")
        home_page.navigate_to_home_page()
        
        # Check if logo is displayed
        if home_page.is_logo_displayed():
            print("✅ Home page loaded successfully")
        else:
            print("❌ Home page failed to load")
            return
        
        # Navigate to login page
        print("🔐 Navigating to login page...")
        login_page.navigate_to_login_page()
        
        # Get valid credentials
        credentials = config.get_valid_credentials()
        print(f"👤 Using credentials: {credentials['username']}")
        
        # Perform login
        print("🔑 Attempting login...")
        success = login_page.login(credentials['username'], credentials['password'])
        
        if success:
            print("✅ Login successful!")
            
            # Check if user is logged in
            if home_page.is_logged_in():
                print("✅ User is logged in")
            else:
                print("❌ User login verification failed")
        else:
            print("❌ Login failed")
        
        # Take a screenshot
        print("📸 Taking screenshot...")
        screenshot_path = screenshot_utils.capture_screenshot("demo", "success")
        print(f"📷 Screenshot saved: {screenshot_path}")
        
        # Wait a bit to see the result
        time.sleep(2)
        
        print("🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        # Take failure screenshot
        try:
            screenshot_utils.capture_screenshot_on_failure("demo", e)
        except:
            pass
    
    finally:
        # Clean up
        print("🧹 Cleaning up...")
        driver_manager.quit_driver()
        print("✅ Demo cleanup completed")


def demo_test_execution():
    """Demonstrate test execution"""
    print("\n🧪 Test Execution Demo")
    print("=" * 30)
    
    print("📋 Available test commands:")
    print("1. Run smoke tests: python run_tests.py --suite smoke")
    print("2. Run regression tests: python run_tests.py --suite regression")
    print("3. Run specific test: python run_tests.py --test tests/testcases/test_login.py")
    print("4. Run with different browser: python run_tests.py --suite smoke --browser firefox")
    print("5. Run in headless mode: python run_tests.py --suite smoke --headless")
    print("6. Run in parallel: python run_tests.py --suite regression --parallel")
    
    print("\n📊 Report locations:")
    print("- HTML Report: tests/reports/html-report/report.html")
    print("- Allure Report: tests/reports/allure-results/")
    print("- Screenshots: tests/reports/screenshots/")


def demo_configuration():
    """Demonstrate configuration options"""
    print("\n⚙️ Configuration Demo")
    print("=" * 25)
    
    config = ConfigReader()
    
    print("🔧 Current configuration:")
    print(f"  Base URL: {config.get_base_url()}")
    print(f"  Browser: {config.get_browser()}")
    print(f"  Headless: {config.get_headless()}")
    print(f"  Implicit Wait: {config.get_implicit_wait()}s")
    print(f"  Explicit Wait: {config.get_explicit_wait()}s")
    
    print("\n📝 To modify configuration:")
    print("1. Edit config/config.ini")
    print("2. Update environment variables in config/environment.env")
    print("3. Use command line arguments with run_tests.py")


def main():
    """Main demo function"""
    print("🎯 E-commerce Automation Framework Demo")
    print("=" * 45)
    
    try:
        # Run basic usage demo
        demo_basic_usage()
        
        # Show test execution options
        demo_test_execution()
        
        # Show configuration options
        demo_configuration()
        
        print("\n🎉 Demo completed! Check the README.md for detailed usage instructions.")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")


if __name__ == "__main__":
    main()
