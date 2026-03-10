#!/usr/bin/env python3
"""
Gemini Vision Test Script
Tests AI vision capabilities
"""

import google.generativeai as genai
from PIL import Image
import cv2
import json
import sys
import os

def test_gemini_vision():
    print("=" * 60)
    print("           👁️ GEMINI VISION TEST SCRIPT")
    print("=" * 60)
    print("\nTesting Gemini Vision AI...\n")
    
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
    print("⚙️  Configuring Gemini AI...")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    print("✅ Gemini Vision initialized!\n")
    
    # Capture photo
    print("📸 Capturing photo from camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Cannot open camera!")
        return False
    
    # Flush buffer
    for _ in range(5):
        cap.read()
    
    ret, frame = cap.read()
    
    if not ret:
        print("❌ Failed to capture image")
        cap.release()
        return False
    
    filename = "vision_test.jpg"
    cv2.imwrite(filename, frame)
    cap.release()
    print(f"✅ Photo captured: {filename}\n")
    
    # Ask AI what it sees
    print("🤖 Asking AI: 'What do you see in this image?'\n")
    
    try:
        img = Image.open(filename)
        
        response = model.generate_content([
            "Describe what you see in this image in detail. Mention objects, colors, and the scene.",
            img
        ])
        
        print("="*60)
        print("AI Response:")
        print("="*60)
        print(response.text)
        print("="*60)
        
        print("\n✅ Vision test complete!")
        print(f"\nImage saved as: {filename}")
        print("Check if AI description matches what camera saw.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check API key")
        print("2. Verify internet connection")
        print("3. Ensure image file was created")
        return False

if __name__ == "__main__":
    success = test_gemini_vision()
    sys.exit(0 if success else 1)