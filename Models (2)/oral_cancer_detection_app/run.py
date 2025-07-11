"""
Run script for Oral Cancer Detection Web Application.
This script ensures the proper environment is set up before running the app.
"""

import os
import sys

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import flask
        import numpy
        import PIL
        print("All core dependencies are installed.")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_environment():
    """Set up the environment for the application."""
    # Create necessary directories if they don't exist
    os.makedirs('uploads', exist_ok=True)
    
    # Set development environment
    os.environ['FLASK_ENV'] = 'development'
    
    print("Environment set up successfully.")
    return True

def main():
    """Main function to run the app."""
    print("Preparing to start Oral Cancer Detection Web App...")
    
    if not check_dependencies():
        return 1
    
    if not setup_environment():
        return 1
    
    print("Starting the application...")
    # Import and run the Flask app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 