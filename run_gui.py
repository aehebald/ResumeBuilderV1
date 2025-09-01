#!/usr/bin/env python3
"""
Startup script for the Resume Generator Web App
"""

import sys
import os
import webbrowser
import threading
import time

def main():
    # Check if virtual environment exists
    venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    
    if not os.path.exists(venv_path):
        print("❌ Virtual environment not found.")
        print("\n🔧 Setting up the application for first run...")
        print("\n1. Create virtual environment:")
        print("   python3 -m venv venv")
        print("\n2. Activate virtual environment:")
        if sys.platform == "win32":
            print("   .\\venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("\n3. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n4. Set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("\n5. Run the application:")
        print("   python run_gui.py")
        return
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OpenAI API key not found!")
        print("\n🔑 Please set your API key:")
        if sys.platform == "win32":
            print("   set OPENAI_API_KEY=your-api-key-here")
        else:
            print("   export OPENAI_API_KEY='your-api-key-here'")
        
        # Try to load from .env file
        try:
            from dotenv import load_dotenv
            load_dotenv()
            if os.getenv('OPENAI_API_KEY'):
                print("✅ API key loaded from .env file")
            else:
                print("\n💡 Alternatively, create a .env file with:")
                print("   OPENAI_API_KEY=your-api-key-here")
                return
        except ImportError:
            print("\n💡 Alternatively, create a .env file with:")
            print("   OPENAI_API_KEY=your-api-key-here")
            return
    
    # Import and run the web app
    try:
        print("🚀 Starting Resume AI Generator Web App...")
        print("🌐 The app will open in your browser automatically")
        
        # Auto-open browser after a short delay
        def open_browser():
            time.sleep(1.5)
            webbrowser.open('http://localhost:5001')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Start the Flask app
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5001)
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\n🔧 Please install required packages:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == '__main__':
    main()