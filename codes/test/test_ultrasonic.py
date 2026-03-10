#!/usr/bin/env python3
"""
Ultrasonic Sensor Test Script
Tests HC-SR04 distance measurements
"""
import RPi.GPIO as GPIO
import time
import sys

def test_ultrasonic():
    print("=" * 60)
    print("           📏 ULTRASONIC SENSOR TEST SCRIPT")
    print("=" * 60)
    print("\nTesting HC-SR04 ultrasonic sensor...\n")
    
    TRIG = 16
    ECHO = 12
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    def get_distance():
        # Send trigger pulse
        GPIO.output(TRIG, False)
        time.sleep(0.00001)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        # Wait for echo
        timeout = time.time() + 0.1
        pulse_start = time.time()
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            if time.time() > timeout:
                return -1
        
        timeout = time.time() + 0.1
        pulse_end = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            if time.time() > timeout:
                return -1
        
        try:
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150  # cm
            return round(distance, 1)
        except:
            return -1
    
    try:
        print("⚠️  REMINDER: ECHO pin must use voltage divider!")
        print("   ECHO → 1kΩ → GPIO 12 → 2kΩ → GND\n")
        print("📏 Move your hand in front of sensor\n")
        print("Press Ctrl+C to stop\n")
        
        successful_reads = 0
        
        for i in range(20):
            dist = get_distance()
            if dist > 0 and dist < 400:
                print(f"Distance: {dist:6.1f} cm")
                successful_reads += 1
            else:
                print("Out of range")
            time.sleep(0.5)
        
        print(f"\n✅ Test complete!")
        print(f"Successful readings: {successful_reads}/20")
        
        if successful_reads >= 15:
            print("✅ Sensor working well!")
            return True
        elif successful_reads >= 10:
            print("⚠️  Sensor partially working")
            return True
        else:
            print("❌ Sensor not working properly")
            print("\nCheck:")
            print("1. Voltage divider circuit")
            print("2. Wiring connections")
            print("3. Sensor power (5V)")
            return False
            
    except KeyboardInterrupt:
        print("\n\nTest stopped by user")
        return True
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    success = test_ultrasonic()
    sys.exit(0 if success else 1)