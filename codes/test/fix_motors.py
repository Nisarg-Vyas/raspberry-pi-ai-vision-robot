#!/usr/bin/env python3
"""
Motor Direction Diagnostic Tool
Tests 4 configurations to find correct motor wiring
"""
import RPi.GPIO as GPIO
import time
import sys

def main():
    print("=" * 60)
    print("           🔧 MOTOR DIRECTION FIXER")
    print("=" * 60)
    print()
    
    # Motor pins
    ENA = 17
    IN1 = 27
    IN2 = 22
    IN3 = 23
    IN4 = 24
    ENB = 18
    
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    for pin in [ENA, IN1, IN2, IN3, IN4, ENB]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    pwm_left = GPIO.PWM(ENA, 100)
    pwm_right = GPIO.PWM(ENB, 100)
    pwm_left.start(0)
    pwm_right.start(0)
    
    def test_config(name, in1, in2, in3, in4):
        print(f"\nTesting: {name}")
        print("Motors should move FORWARD")
        input("Press Enter when ready...")
        
        pwm_left.ChangeDutyCycle(50)
        pwm_right.ChangeDutyCycle(50)
        GPIO.output(IN1, in1)
        GPIO.output(IN2, in2)
        GPIO.output(IN3, in3)
        GPIO.output(IN4, in4)
        
        time.sleep(2)
        
        pwm_left.ChangeDutyCycle(0)
        pwm_right.ChangeDutyCycle(0)
        
        result = input("Did it move FORWARD? (y/n): ")
        return result.lower() == 'y'
    
    # Test different configurations
    configs = [
        ("Config 1", GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW),
        ("Config 2", GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH),
        ("Config 3", GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH),
        ("Config 4", GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW),
    ]
    
    print("\nWe'll test 4 configurations.")
    print("Watch your robot and tell me which moves FORWARD correctly.\n")
    
    correct_config = None
    
    try:
        for config in configs:
            if test_config(*config):
                correct_config = config
                print(f"\n✅ {config[0]} is CORRECT!")
                break
        
        if correct_config:
            print(f"\n📝 Use these values in your code:")
            print(f"   GPIO.output(self.IN1, {correct_config[1]})")
            print(f"   GPIO.output(self.IN2, {correct_config[2]})")
            print(f"   GPIO.output(self.IN3, {correct_config[3]})")
            print(f"   GPIO.output(self.IN4, {correct_config[4]})")
            return True
        else:
            print("\n⚠️  None worked? Check your wiring!")
            return False
            
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
        return False
    finally:
        pwm_left.stop()
        pwm_right.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)