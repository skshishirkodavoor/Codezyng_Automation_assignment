# E-commerce Automation Framework

A comprehensive Selenium automation framework built with Python and pytest for testing e-commerce web applications.

### 1. Install Dependencies
pip install -r requirements.txt

### 2. Test Installation
python simple_demo.py

### 3. Run Tests

# (i) Run smoke tests
python run_tests.py --suite smoke

# (ii) Run with specific browser
python run_tests.py --suite smoke --browser firefox

# (iii) Run in headless mode
python run_tests.py --suite smoke --headless

## 📁 Project Structure

ecommerce_automation_framework/
├── config/                     # Configuration files
│   └── config.ini             # Main configuration
├── tests/                      # Test implementation
│   ├── pages/                 # Page Object Model
│   ├── testcases/             # Test cases
│   ├── data/                  # Test data
│   └── reports/               # Test reports
├── utils/                     # Utility classes
│   ├── driver_manager.py
│   ├── config_reader.py
│   └── ...
├── requirements.txt           # Dependencies
├── install.py                 # Installation script
├── run_tests.py              # Test runner
└── README.md                 # This file


## 🔧 Configuration

Edit `config/config.ini` to configure your test environment:

```ini
[ENVIRONMENT]
base_url = https://demo.opencart.com/
browser = chrome
headless = false
```

##  Available Test Suites

- **Smoke Tests**: Critical functionality (`--suite smoke`)
- **Regression Tests**: Complete test suite (`--suite regression`)
- **Sanity Tests**: Basic functionality (`--suite sanity`)

##  Reports

- **HTML Report**: `tests/reports/html-report/report.html`
- **Allure Report**: `allure serve tests/reports/allure-results`

##  Features

-  Page Object Model (POM)
-  Multi-browser support (Chrome, Firefox, Edge)
-  Parallel test execution
-  Data-driven testing
-  Comprehensive reporting
-  Screenshot capture on failures
-  CI/CD integration ready

