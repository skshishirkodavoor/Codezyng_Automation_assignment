import os
import sys
import subprocess
import argparse
from pathlib import Path
from loguru import logger


class TestRunner:
    """Test runner for executing different test suites"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "tests" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def run_smoke_tests(self, browser="chrome", headless=False, parallel=False):
        """Run smoke tests"""
        logger.info("Running smoke tests...")
        cmd = self._build_command(
            markers="smoke",
            browser=browser,
            headless=headless,
            parallel=parallel
        )
        return self._execute_command(cmd, "smoke")
    
    def run_regression_tests(self, browser="chrome", headless=False, parallel=True):
        """Run regression tests"""
        logger.info("Running regression tests...")
        cmd = self._build_command(
            markers="regression",
            browser=browser,
            headless=headless,
            parallel=parallel
        )
        return self._execute_command(cmd, "regression")
    
    def run_sanity_tests(self, browser="chrome", headless=False, parallel=False):
        """Run sanity tests"""
        logger.info("Running sanity tests...")
        cmd = self._build_command(
            markers="sanity",
            browser=browser,
            headless=headless,
            parallel=parallel
        )
        return self._execute_command(cmd, "sanity")
    
    def run_specific_tests(self, test_path, browser="chrome", headless=False, parallel=False):
        """Run specific test file or test function"""
        logger.info(f"Running specific tests: {test_path}")
        cmd = self._build_command(
            test_path=test_path,
            browser=browser,
            headless=headless,
            parallel=parallel
        )
        return self._execute_command(cmd, "specific")
    
    def run_all_tests(self, browser="chrome", headless=False, parallel=True):
        """Run all tests"""
        logger.info("Running all tests...")
        cmd = self._build_command(
            browser=browser,
            headless=headless,
            parallel=parallel
        )
        return self._execute_command(cmd, "all")
    
    def _build_command(self, markers=None, test_path=None, browser="chrome", headless=False, parallel=False):
        """Build pytest command"""
        cmd = ["python", "-m", "pytest"]
        
        # Add markers
        if markers:
            cmd.extend(["-m", markers])
        
        # Add test path
        if test_path:
            cmd.append(test_path)
        
        # Add browser and headless options
        cmd.extend(["--browser", browser])
        if headless:
            cmd.append("--headless")
        
        # Add parallel execution
        if parallel:
            cmd.extend(["-n", "auto"])
        
        # Add additional options
        cmd.extend([
            "--tb=short",
            "--capture=no",
            "--html=tests/reports/html-report/report.html",
            "--self-contained-html"
        ])
        
        return cmd
    
    def _execute_command(self, cmd, test_type):
        """Execute pytest command"""
        try:
            logger.info(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            
            # Log output
            if result.stdout:
                logger.info(f"STDOUT: {result.stdout}")
            if result.stderr:
                logger.error(f"STDERR: {result.stderr}")
            
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Failed to execute command: {str(e)}")
            return False
    
    def open_reports(self):
        """Open generated reports"""
        try:
            # Open HTML report
            html_report = self.reports_dir / "html-report" / "report.html"
            if html_report.exists():
                import webbrowser
                webbrowser.open(f"file://{html_report.absolute()}")
                logger.info("Opened HTML report")
            
        except Exception as e:
            logger.error(f"Failed to open reports: {str(e)}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="E-commerce Automation Test Runner")
    parser.add_argument("--suite", choices=["smoke", "regression", "sanity", "all"], 
                       default="smoke", help="Test suite to run")
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge"], 
                       default="chrome", help="Browser to use")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--test", help="Specific test file or function to run")
    parser.add_argument("--open-reports", action="store_true", help="Open reports after execution")
    
    args = parser.parse_args()
    
    # Setup logging
    logger.add("tests/reports/test_runner.log", rotation="1 day", retention="7 days")
    
    runner = TestRunner()
    success = False
    
    try:
        if args.test:
            success = runner.run_specific_tests(
                test_path=args.test,
                browser=args.browser,
                headless=args.headless,
                parallel=args.parallel
            )
        elif args.suite == "smoke":
            success = runner.run_smoke_tests(
                browser=args.browser,
                headless=args.headless,
                parallel=args.parallel
            )
        elif args.suite == "regression":
            success = runner.run_regression_tests(
                browser=args.browser,
                headless=args.headless,
                parallel=args.parallel
            )
        elif args.suite == "sanity":
            success = runner.run_sanity_tests(
                browser=args.browser,
                headless=args.headless,
                parallel=args.parallel
            )
        elif args.suite == "all":
            success = runner.run_all_tests(
                browser=args.browser,
                headless=args.headless,
                parallel=args.parallel
            )
        
        if args.open_reports:
            runner.open_reports()
        
        if success:
            logger.info("Test execution completed successfully")
            sys.exit(0)
        else:
            logger.error("Test execution failed")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Test execution failed with error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()