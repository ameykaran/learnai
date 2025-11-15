#!/usr/bin/env python3

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    packages = [
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "sqlalchemy==2.0.23",
        "pydantic==2.5.0",
        "python-multipart==0.0.6"
    ]

    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--break-system-packages"])
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")
            return False

    return True

def run_server():
    """Run the FastAPI server"""
    try:
        print("Starting FastAPI server...")
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error running server: {e}")

if __name__ == "__main__":
    print("Setting up and running the Quiz Backend...")

    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        print("Installing dependencies...")
        if install_dependencies():
            print("Dependencies installed successfully!")
        else:
            print("Failed to install some dependencies.")
            sys.exit(1)

    run_server()