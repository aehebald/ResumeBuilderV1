#!/usr/bin/env python3
"""
Simple script to help set up OpenAI API key
"""

import os

def setup_api_key():
    print("🔑 OPENAI API KEY SETUP")
    print("=" * 40)
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content and not content.count('your_openai_api_key_here'):
                print("✅ API key appears to be set")
                return
    
    print("📝 Setting up your OpenAI API key...")
    print("\n🔗 To get your API key:")
    print("   1. Go to https://platform.openai.com/api-keys")
    print("   2. Sign in to your OpenAI account")
    print("   3. Click 'Create new secret key'")
    print("   4. Copy the key (starts with 'sk-')")
    
    api_key = input("\n🔑 Enter your OpenAI API key: ").strip()
    
    if not api_key.startswith('sk-'):
        print("⚠️  Warning: API key should start with 'sk-'")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            print("❌ Setup cancelled")
            return
    
    # Write to .env file
    env_content = f"OPENAI_API_KEY={api_key}\n"
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ API key saved to {env_file}")
    print("\n🧪 You can now run the API tests:")
    print("   python test_api.py")
    
    print("\n⚠️  IMPORTANT: Keep your API key secret!")
    print("   - Never commit .env to git")
    print("   - Don't share your API key with others")

if __name__ == '__main__':
    setup_api_key()