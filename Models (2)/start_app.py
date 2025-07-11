"""
Simple script to start the Oral Cancer Detection web application.
This script is designed to be very simple to avoid import errors.
"""

import os
import sys

# Create uploads folder if it doesn't exist
os.makedirs('uploads', exist_ok=True)

# Import and run the Flask app
print("Starting Oral Cancer Detection Web App on port 8000...")
from app import app
app.run(debug=True, host='0.0.0.0', port=8000) 