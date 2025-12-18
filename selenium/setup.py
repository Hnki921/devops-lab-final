"""
Selenium Test Setup and Configuration for Todo List Application
This script helps set up and run Selenium tests
"""

import subprocess
import sys
import os
from pathlib import Path

class SeleniumTestSetup:
    """Setup and configuration for Selenium tests"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.requirements = [
            'selenium>=4.0.0',
            'webdriver-manager>=3.8.0',
            'requests>=2.28.0',
            'pytest>=7.0.0',
            'pytest-html>=3.1.1'
        ]
    
    def install_requirements(self):
        """Install required Python packages"""
        print("Installing Selenium test dependencies...")
        for requirement in self.requirements:
            try:
                subprocess.check_call(
                    [sys.executable, '-m', 'pip', 'install', requirement]
                )
                print(f"✓ Installed: {requirement}")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install {requirement}: {e}")
                return False
        return True
    
    def verify_installation(self):
        """Verify all required packages are installed"""
        print("\nVerifying installation...")
        missing = []
        
        try:
            import selenium
            print("✓ Selenium installed")
        except ImportError:
            missing.append("selenium")
            print("✗ Selenium not installed")
        
        try:
            import webdriver_manager
            print("✓ WebDriver Manager installed")
        except ImportError:
            missing.append("webdriver-manager")
            print("✗ WebDriver Manager not installed")
        
        try:
            import pytest
            print("✓ Pytest installed")
        except ImportError:
            missing.append("pytest")
            print("✗ Pytest not installed")
        
        return len(missing) == 0
    
    def run_tests(self, app_url="http://localhost:8000"):
        """Run Selenium test suite"""
        print(f"\n{'='*60}")
        print(f"Running Selenium Tests for Todo Application")
        print(f"Target URL: {app_url}")
        print(f"{'='*60}\n")
        
        # Set environment variable for test URL
        os.environ['APP_URL'] = app_url
        
        test_file = self.base_dir / 'test_todo_application.py'
        
        if not test_file.exists():
            print(f"✗ Test file not found: {test_file}")
            return False
        
        try:
            # Run with unittest
            subprocess.run(
                [sys.executable, str(test_file)],
                check=False
            )
            return True
        except Exception as e:
            print(f"✗ Error running tests: {e}")
            return False
    
    def run_tests_with_pytest(self, app_url="http://localhost:8000"):
        """Run tests using pytest (generates HTML report)"""
        print(f"\n{'='*60}")
        print(f"Running Selenium Tests with Pytest")
        print(f"Target URL: {app_url}")
        print(f"{'='*60}\n")
        
        os.environ['APP_URL'] = app_url
        
        test_file = self.base_dir / 'test_todo_application.py'
        report_file = self.base_dir / 'test_report.html'
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pytest',
                str(test_file),
                '-v',
                f'--html={report_file}',
                '--self-contained-html'
            ])
            print(f"\n✓ Test report generated: {report_file}")
            return True
        except Exception as e:
            print(f"✗ Error running pytest: {e}")
            return False

def main():
    """Main setup and execution function"""
    print("="*60)
    print("SELENIUM TEST SUITE SETUP")
    print("="*60 + "\n")
    
    setup = SeleniumTestSetup()
    
    # Step 1: Install requirements
    print("Step 1: Installing requirements...")
    if not setup.install_requirements():
        print("Failed to install requirements")
        return False
    
    # Step 2: Verify installation
    print("\nStep 2: Verifying installation...")
    if not setup.verify_installation():
        print("Some packages are missing")
        return False
    
    print("\n✓ All dependencies installed successfully!\n")
    
    # Step 3: Run tests
    app_url = input("Enter application URL (default: http://localhost:8000): ").strip()
    if not app_url:
        app_url = "http://localhost:8000"
    
    print(f"\nRunning tests against: {app_url}")
    setup.run_tests(app_url)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
