#!/usr/bin/env python3
"""
Setup script for DOGE API Data Export Tool
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def create_directory(directory):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
        return True
    except Exception as e:
        print(f"❌ Failed to create directory {directory}: {str(e)}")
        return False


def create_virtual_env():
    """Create virtual environment"""
    try:
        if os.path.exists("venv"):
            print("⚠️ Virtual environment already exists.")
            return True

        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✅ Virtual environment created.")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {str(e)}")
        return False


def install_requirements():
    """Install requirements"""
    try:
        print("Installing requirements...")

        # Determine the pip path based on OS
        if os.name == "nt":  # Windows
            pip_path = os.path.join("venv", "Scripts", "pip")
        else:  # Unix/Linux/MacOS
            pip_path = os.path.join("venv", "bin", "pip")

        subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
        print("✅ Requirements installed.")
        return True
    except Exception as e:
        print(f"❌ Failed to install requirements: {str(e)}")
        return False


def create_env_file():
    """Create .env file from sample if it doesn't exist"""
    try:
        if os.path.exists(".env"):
            print("⚠️ .env file already exists.")
            return True

        if os.path.exists(".env.sample"):
            shutil.copy(".env.sample", ".env")
            print("✅ Created .env file from sample.")
            return True
        else:
            print("❌ .env.sample file not found.")
            return False
    except Exception as e:
        print(f"❌ Failed to create .env file: {str(e)}")
        return False


def create_data_directory():
    """Create data directory"""
    return create_directory("doge_data")


def main():
    """Main setup function"""
    print("Setting up DOGE API Data Export Tool...")

    # Create virtual environment
    if not create_virtual_env():
        print("⚠️ Setup will continue but might not be complete.")

    # Install requirements
    if not install_requirements():
        print("⚠️ Setup will continue but might not be complete.")

    # Create .env file
    if not create_env_file():
        print("⚠️ Setup will continue but might not be complete.")

    # Create data directory
    if not create_data_directory():
        print("⚠️ Setup will continue but might not be complete.")

    print("\nSetup complete! To activate the virtual environment:")

    if os.name == "nt":  # Windows
        print("\n  venv\\Scripts\\activate")
    else:  # Unix/Linux/MacOS
        print("\n  source venv/bin/activate")

    print("\nTo update API settings, edit the .env file.")
    print("\nTo run the tool:")
    print("\n  python doge_api_processor.py --all")
    print("  python doge_api_processor.py --data-type departments")
    print("  python example_usage.py")


if __name__ == "__main__":
    main()
