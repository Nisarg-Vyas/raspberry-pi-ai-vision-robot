#!/usr/bin/env python3
"""
Microphone Test Script
Tests speech recognition from microphone
"""

import speech_recognition as sr
import sys

def test_microphone():
    print("=" * 60)
    print("           🎤 MICROPHONE TEST SCRIPT")
    print("=" * 60)
    print("\nTesting microphone and speech recognition...\n")
    print("Make sure your Bluetooth speaker has a working microphone!\n")
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 4000
    
    # Test 3 times
    successful_tests = 0
    
    for i in range(3):
        print(f"\n{'='*60}")
        print(f"           TEST {i+1}/3")
        print(f"{'='*60}\n")
        
        with sr.Microphone() as source:
            print("🔇 Adjusting for ambient noise... (wait 2 seconds)")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("👂 Listening... SPEAK NOW!")
            print("   (Say something clearly into the microphone)")
            
            try:
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)
                print("⏳ Processing...")
                
                # Convert speech to text
                text = recognizer.recognize_google(audio)
                print(f"✅ SUCCESS! You said: \"{text}\"")
                successful_tests += 1
                
            except sr.WaitTimeoutError:
                print("⏰ No speech detected (timeout)")
                print("   Try speaking louder or closer to microphone")
            except sr.UnknownValueError:
                print("❓ Could not understand audio")
                print("   Try speaking more clearly")
            except sr.RequestError as e:
                print(f"❌ Network error: {e}")
                print("   Check internet connection")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("           TEST RESULTS")
    print("="*60)
    print(f"\nSuccessful: {successful_tests}/3")
    
    if successful_tests >= 2:
        print("✅ Microphone is working well!")
        return True
    elif successful_tests == 1:
        print("⚠️  Microphone partially working")
        print("   Try adjusting microphone sensitivity or speaking louder")
        return True
    else:
        print("❌ Microphone test failed")
        print("\nTroubleshooting:")
        print("1. Check Bluetooth connection")
        print("2. Ensure microphone is not muted")
        print("3. Test with: arecord -l")
        print("4. Speak louder and closer to mic")
        print("5. Check internet connection (Google Speech needs it)")
        return False

if __name__ == "__main__":
    success = test_microphone()
    sys.exit(0 if success else 1)