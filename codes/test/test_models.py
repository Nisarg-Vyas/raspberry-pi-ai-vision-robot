#!/usr/bin/env python3
"""
Gemini Models Checker
Lists all available Gemini models for your API key
"""
import google.generativeai as genai
import json
import sys
import os

def check_models():
    print("=" * 60)
    print("           📋 GEMINI MODELS CHECKER")
    print("=" * 60)
    print()
    
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
            return False
    except Exception as e:
        print(f"❌ ERROR loading config: {e}")
        return False
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    print("Available Gemini Models:")
    print("=" * 60)
    
    model_count = 0
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            model_count += 1
    
    print("=" * 60)
    print(f"\nTotal models available: {model_count}")
    
    print("\nRecommended models:")
    print("  • models/gemini-2.0-flash (fast, vision support)")
    print("  • models/gemini-2.5-flash (newer version)")
    print("  • models/gemini-2.5-pro (most capable)")
    
    return True

if __name__ == "__main__":
    success = check_models()
    sys.exit(0 if success else 1)