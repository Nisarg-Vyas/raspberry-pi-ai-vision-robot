#!/usr/bin/env python3
"""
Motor Test Script
Tests all four motor movements: forward, backward, left, right
"""
import RPi.GPIO as GPIO
import time
import sys

def test_motors():
    print("=" * 60)
    print("           🚗 MOTOR TEST SCRIPT")
    print("=" * 60)
    print("\nTesting motor movements...\n")
    
    # Motor pins
    ENA = 17  # Left motors speed
    IN1 = 27  # Left motors direction
    IN2 = 22
    IN3 = 23  # Right motors direction
    IN4 = 24
    ENB = 18  # Right motors speed
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup pins
    for pin in [ENA, IN1, IN2, IN3, IN4, ENB]:
        GPIO.setup(pin, GPIO.OUT)
    
    # PWM for speed control
    pwm_left = GPIO.PWM(ENA, 100)
    pwm_right = GPIO.PWM(ENB, 100)
    pwm_left.start(0)
    pwm_right.start(0)
    
    def forward(speed=60, duration=2):
        print(f"▶️  Moving forward at {speed}% for {duration}s")
        pwm_left.ChangeDutyCycle(speed)
        pwm_right.ChangeDutyCycle(speed)
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        time.sleep(duration)
    
    def backward(speed=60, duration=2):
        print(f"◀️  Moving backward at {speed}% for {duration}s")
        pwm_left.ChangeDutyCycle(speed)
        pwm_right.ChangeDutyCycle(speed)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        time.sleep(duration)
    
    def turn_left(speed=60, duration=1):
        print(f"↪️  Turning left at {speed}% for {duration}s")
        pwm_left.ChangeDutyCycle(speed)
        pwm_right.ChangeDutyCycle(speed)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        time.sleep(duration)
    
    def turn_right(speed=60, duration=1):
        print(f"↩️  Turning right at {speed}% for {duration}s")
        pwm_left.ChangeDutyCycle(speed)
        pwm_right.ChangeDutyCycle(speed)
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        time.sleep(duration)
    
    def stop():
        print("⏹️  Stopping")
        pwm_left.ChangeDutyCycle(0)
        pwm_right.ChangeDutyCycle(0)
    
    # Test sequence
    try:
        print("Starting motor test sequence...\n")
        
        forward(50, 2)
        stop()
        time.sleep(1)
        
        backward(50, 2)
        stop()
        time.sleep(1)
        
        turn_left(50, 1.5)
        stop()
        time.sleep(1)
        
        turn_right(50, 1.5)
        stop()
        
        print("\n✅ Motor test complete!")
        print("\nDid all movements work correctly?")
        print("If robot turned instead of going forward, run:")
        print("   python tests/fix_motors.py")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\nTest stopped by user")
        return False
    finally:
        stop()
        pwm_left.stop()
        pwm_right.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    success = test_motors()
    sys.exit(0 if success else 1)