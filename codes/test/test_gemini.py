#!/usr/bin/env python3
"""
Gemini AI Test Script
Tests Google Gemini API text responses
"""

import google.generativeai as genai
import json
import sys
import os

def test_gemini():
    print("=" * 60)
    print("           🤖 GEMINI AI TEST SCRIPT")
    print("=" * 60)
    print("\nTesting Google Gemini API...\n")
    
    # Load API key
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
                api_key = config['gemini_api_key']
        elif os.path.exists('../config.json'):
            with open('../config.json', 'r') as f:
                config = json.load(f)
                api_key = config['gemini_api_key']
        else:
            print("❌ ERROR: config.json not found!")
            print("\nCreate config.json with:")
            print('{"gemini_api_key": "YOUR_KEY_HERE"}')
            return False
    except KeyError:
        print("❌ ERROR: 'gemini_api_key' not found in config.json")
        return False
    except Exception as e:
        print(f"❌ ERROR loading config: {e}")
        return False
    
    # Configure Gemini
    print("⚙️  Configuring Gemini AI...")
    genai.configure(api_key=api_key)
    
    # Create model
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        print("✅ Gemini initialized!\n")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nTry running: python tests/check_models.py")
        return False
    
    # Test questions
    questions = [
        "What is 5 + 7?",
        "What is a robot in one sentence?",
        "Tell me a very short joke about robots"
    ]
    
    successful_tests = 0
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"Question {i}/{len(questions)}")
        print(f"{'='*60}")
        print(f"Q: {question}")
        
        try:
            response = model.generate_content(question)
            print(f"A: {response.text}\n")
            print("✅ Success!")
            successful_tests += 1
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    print("\n" + "="*60)
    print("           TEST RESULTS")
    print("="*60)
    print(f"\nSuccessful: {successful_tests}/{len(questions)}")
    
    if successful_tests == len(questions):
        print("✅ Gemini AI test complete!")
        return True
    else:
        print("❌ Some tests failed")
        print("\nTroubleshooting:")
        print("1. Check API key in config.json")
        print("2. Verify internet connection")
        print("3. Check API quota: https://ai.google.dev/")
        return False

if __name__ == "__main__":
    success = test_gemini()
    sys.exit(0 if success else 1)