#!/usr/bin/env python3
"""
Voice Selection Tool
Lists and tests different TTS voices
"""
import pyttsx3
import sys

def test_voices():
    print("=" * 60)
    print("           🗣️ VOICE SELECTION TOOL")
    print("=" * 60)
    print()
    
    try:
        engine = pyttsx3.init()
        
        # List available voices
        voices = engine.getProperty('voices')
        print(f"Found {len(voices)} available voice(s):\n")
        
        for i, voice in enumerate(voices):
            print(f"{i}: {voice.name}")
            print(f"   ID: {voice.id}")
            print(f"   Languages: {voice.languages}")
            print()
        
        # Test each voice
        test_text = "Hello, I am your robot assistant"
        
        print("\nTesting each voice with:")
        print(f'"{test_text}"\n')
        
        for i, voice in enumerate(voices):
            print(f"Playing voice {i}...")
            engine.setProperty('voice', voice.id)
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            engine.say(test_text)
            engine.runAndWait()
            input("Press Enter for next voice...")
        
        print("\n✅ Voice test complete!")
        print("\nTo use a specific voice in your robot:")
        print("1. Note the voice number you prefer")
        print("2. In robot code, add:")
        print("   voices = self.engine.getProperty('voices')")
        print("   self.engine.setProperty('voice', voices[NUMBER].id)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_voices()
    sys.exit(0 if success else 1)