"""
Installation script for E-commerce Automation Framework
"""
import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_requirements():
    """Install Python requirements"""
    if not run_command("pip install -r requirements.txt", "Installing Python requirements"):
        return False
    return True


def install_allure():
    """Install Allure reporting tool"""
    system = platform.system().lower()
    
    if system == "windows":
        # Check if Chocolatey is installed
        if run_command("choco --version", "Checking Chocolatey"):
            return run_command("choco install allure -y", "Installing Allure via Chocolatey")
        else:
            print("⚠️  Chocolatey not found. Please install Allure manually from https://docs.qameta.io/allure/")
            return True
    elif system == "darwin":  # macOS
        # Check if Homebrew is installed
        if run_command("brew --version", "Checking Homebrew"):
            return run_command("brew install allure", "Installing Allure via Homebrew")
        else:
            print("⚠️  Homebrew not found. Please install Allure manually from https://docs.qameta.io/allure/")
            return True
    elif system == "linux":
        return run_command("sudo apt-get update && sudo apt-get install -y allure", "Installing Allure via apt-get")
    else:
        print(f"⚠️  Unsupported OS: {system}. Please install Allure manually from https://docs.qameta.io/allure/")
        return True


def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        "tests/reports/html-report",
        "tests/reports/allure-results",
        "tests/reports/screenshots",
        "tests/data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True


def generate_sample_data():
    """Generate sample test data"""
    print("📊 Generating sample test data...")
    try:
        import sys
        sys.path.append(str(Path.cwd()))
        from tests.data.sample_test_data import create_sample_test_data
        create_sample_test_data()
        print("✅ Sample test data generated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to generate sample data: {str(e)}")
        return False


def verify_installation():
    """Verify installation by running a simple test"""
    print("🧪 Verifying installation...")
    try:
        # Try to import key modules
        from utils.driver_manager import DriverManager
        from utils.config_reader import ConfigReader
        from tests.pages.base_page import BasePage
        print("✅ All modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Installation verification failed: {str(e)}")
        return False


def main():
    """Main installation function"""
    print("🚀 E-commerce Automation Framework Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Install Allure
    if not install_allure():
        print("⚠️  Allure installation failed, but continuing...")
    
    # Generate sample data
    if not generate_sample_data():
        print("⚠️  Failed to generate sample data, but continuing...")
    
    # Verify installation
    if not verify_installation():
        print("❌ Installation verification failed")
        sys.exit(1)
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Configure your test environment in config/config.ini")
    print("2. Run smoke tests: python run_tests.py --suite smoke")
    print("3. Check the README.md for detailed usage instructions")
    print("\nHappy Testing! 🚀")


if __name__ == "__main__":
    main()