#!/usr/bin/env python3
"""
Main entry point for Replit deployment
"""

from app import app
import os

if __name__ == '__main__':
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set!")
        print("Please set it in the Secrets tab of your Replit project")
        print("Key: OPENAI_API_KEY")
        print("Value: your-actual-api-key")
    
    print("🚀 Starting Resume AI Generator Web App on Replit...")
    print("🌐 The app will be available at your Replit URL")
    app.run(host='0.0.0.0', port=5001, debug=False)