#!/usr/bin/env python3
"""
Speaker Test Script
Tests audio output with text-to-speech
"""
import pyttsx3
import sys
import time

def test_speaker():
    print("=" * 60)
    print("           🔊 SPEAKER TEST SCRIPT")
    print("=" * 60)
    print("\nTesting speaker output...\n")
    
    try:
        print("⚙️  Initializing text-to-speech engine...")
        engine = pyttsx3.init()
        
        # Set properties
        engine.setProperty('rate', 150)  # Speed
        engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        print("✅ Engine initialized!\n")
        
        # Test phrases
        test_phrases = [
            "Hello, I am your robot",
            "Audio test successful",
            "Motor control ready",
            "Sensor initialized"
        ]
        
        print("🔊 Playing test phrases...\n")
        
        for i, phrase in enumerate(test_phrases, 1):
            print(f"   {i}. {phrase}")
            engine.say(phrase)
            engine.runAndWait()
            time.sleep(0.5)
        
        print("\n✅ Speaker test complete!")
        print("\nDid you hear all 4 phrases clearly?")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check Bluetooth speaker connection")
        print("2. Check volume levels: alsamixer")
        print("3. Reconnect Bluetooth: bluetoothctl")
        return False

if __name__ == "__main__":
    success = test_speaker()
    sys.exit(0 if success else 1)