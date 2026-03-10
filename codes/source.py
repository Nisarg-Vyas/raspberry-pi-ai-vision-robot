import speech_recognition as sr
from gtts import gTTS
import pygame
import google.generativeai as genai
from PIL import Image
import cv2
import RPi.GPIO as GPIO
import json
import time
import os
import re
import threading

class AdvancedAIRobot:
    def __init__(self, api_key):
        print("🤖 Initializing Advanced AI Robot...")
        
        # Speech recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        
        # Text-to-speech
        pygame.mixer.init()
        
        # Camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Motor setup
        self.setup_motors()
        
        # Gemini AI
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.0-flash')
        
        # State management
        self.is_speaking = False
        self.should_stop_speaking = False
        self.last_response = ""
        self.last_position = 0
        self.speaking_thread = None
        self.speech_lock = threading.Lock()
        
        print("✅ Robot ready!\n")
    
    def setup_motors(self):
        """Initialize motor pins with correct configuration"""
        self.ENA = 17  # Left motors PWM
        self.IN1 = 27  # Left motor control
        self.IN2 = 22
        self.IN3 = 23  # Right motor control
        self.IN4 = 24
        self.ENB = 18  # Right motors PWM
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        for pin in [self.ENA, self.IN1, self.IN2, self.IN3, self.IN4, self.ENB]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        
        self.pwm_left = GPIO.PWM(self.ENA, 100)
        self.pwm_right = GPIO.PWM(self.ENB, 100)
        self.pwm_left.start(0)
        self.pwm_right.start(0)
        
        print("✅ Motors initialized")
    
    def move_forward(self, speed=60, duration=2):
        """Move forward - FIXED direction"""
        print(f"🚗 Moving forward ({duration}s at {speed}%)")
        
        # Set speed
        self.pwm_left.ChangeDutyCycle(speed)
        self.pwm_right.ChangeDutyCycle(speed)
        
        # Both motors forward
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
        time.sleep(duration)
        self.stop_motors()
    
    def move_backward(self, speed=60, duration=2):
        """Move backward - FIXED direction"""
        print(f"🚗 Moving backward ({duration}s at {speed}%)")
        
        self.pwm_left.ChangeDutyCycle(speed)
        self.pwm_right.ChangeDutyCycle(speed)
        
        # Both motors backward
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        
        time.sleep(duration)
        self.stop_motors()
    
    def turn_left(self, speed=60, duration=1):
        """Turn left - left motors backward, right forward"""
        print(f"🚗 Turning left ({duration}s at {speed}%)")
        
        self.pwm_left.ChangeDutyCycle(speed)
        self.pwm_right.ChangeDutyCycle(speed)
        
        # Left backward, right forward
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
        time.sleep(duration)
        self.stop_motors()
    
    def turn_right(self, speed=60, duration=1):
        """Turn right - left forward, right backward"""
        print(f"🚗 Turning right ({duration}s at {speed}%)")
        
        self.pwm_left.ChangeDutyCycle(speed)
        self.pwm_right.ChangeDutyCycle(speed)
        
        # Left forward, right backward
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        
        time.sleep(duration)
        self.stop_motors()
    
    def stop_motors(self):
        """Stop all motors"""
        self.pwm_left.ChangeDutyCycle(0)
        self.pwm_right.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
    
    def test_motor_directions(self):
        """Test and verify motor directions"""
        self.speak("Testing motor directions. Watch carefully", interruptible=False)
        
        print("\n=== MOTOR DIRECTION TEST ===")
        
        # Test forward
        self.speak("Testing forward", interruptible=False)
        self.move_forward(50, 2)
        time.sleep(1)
        
        # Test backward
        self.speak("Testing backward", interruptible=False)
        self.move_backward(50, 2)
        time.sleep(1)
        
        # Test left
        self.speak("Testing left turn", interruptible=False)
        self.turn_left(50, 1)
        time.sleep(1)
        
        # Test right
        self.speak("Testing right turn", interruptible=False)
        self.turn_right(50, 1)
        time.sleep(1)
        
        self.speak("Motor test complete", interruptible=False)
    
    def speak(self, text, interruptible=True):
        """Text to speech with interrupt support"""
        print(f"🤖 Robot: {text}")
        
        if not interruptible:
            self._speak_now(text)
            return
        
        # Store for continue feature
        self.last_response = text
        self.last_position = 0
        
        # Start speaking in background thread
        with self.speech_lock:
            self.is_speaking = True
            self.should_stop_speaking = False
        
        self.speaking_thread = threading.Thread(target=self._speak_interruptible, args=(text,))
        self.speaking_thread.daemon = True
        self.speaking_thread.start()
    
    def _speak_now(self, text):
        """Direct speech without interruption"""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            speech_file = f"speech_{int(time.time())}.mp3"
            tts.save(speech_file)
            
            pygame.mixer.music.load(speech_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.unload()
            
            # Clean up file
            try:
                time.sleep(0.2)
                if os.path.exists(speech_file):
                    os.remove(speech_file)
            except:
                pass
                
        except Exception as e:
            print(f"Speech error: {e}")
    
    def _speak_interruptible(self, text):
        """Speak with ability to be interrupted"""
        try:
            # Split into sentences for granular interruption
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            for i, sentence in enumerate(sentences):
                with self.speech_lock:
                    if self.should_stop_speaking:
                        self.last_position = i
                        break
                
                speech_file = f"speech_{int(time.time())}_{i}.mp3"
                
                try:
                    tts = gTTS(text=sentence, lang='en', slow=False)
                    tts.save(speech_file)
                    
                    pygame.mixer.music.load(speech_file)
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        with self.speech_lock:
                            if self.should_stop_speaking:
                                pygame.mixer.music.stop()
                                self.last_position = i
                                break
                        time.sleep(0.1)
                    
                    pygame.mixer.music.unload()
                    
                    # Clean up
                    try:
                        time.sleep(0.2)
                        if os.path.exists(speech_file):
                            os.remove(speech_file)
                    except:
                        pass
                    
                    with self.speech_lock:
                        if self.should_stop_speaking:
                            break
                            
                except Exception as e:
                    print(f"Sentence speech error: {e}")
            
            with self.speech_lock:
                self.is_speaking = False
                
        except Exception as e:
            print(f"Speech error: {e}")
            with self.speech_lock:
                self.is_speaking = False
    
    def stop_speaking(self):
        """Stop current speech"""
        with self.speech_lock:
            if self.is_speaking:
                self.should_stop_speaking = True
                pygame.mixer.music.stop()
                print("🛑 Speech interrupted")
        
        time.sleep(0.3)
        self.speak("Okay, stopping", interruptible=False)
    
    def continue_speaking(self):
        """Continue from where we left off"""
        if not self.last_response:
            self.speak("I wasn't saying anything", interruptible=False)
            return
        
        sentences = re.split(r'[.!?]+', self.last_response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if self.last_position < len(sentences):
            remaining = ". ".join(sentences[self.last_position:])
            self.speak(f"Continuing. {remaining}")
        else:
            self.speak("I already finished what I was saying", interruptible=False)
    
    def scan_surroundings(self):
        """Rotate 360 degrees, take photos, and describe what was seen"""
        self.speak("Scanning surroundings in 360 degrees", interruptible=False)
        
        num_photos = 8  # Take 8 photos (every 45 degrees)
        rotation_time = 0.5  # Time to rotate ~45 degrees
        
        descriptions = []
        
        for i in range(num_photos):
            print(f"📸 Photo {i+1}/{num_photos}")
            
            # Capture image
            img_path = self.capture_image(f"scan_{i+1}")
            
            if img_path:
                # Get AI description
                try:
                    img = Image.open(img_path)
                    response = self.model.generate_content([
                        "Briefly describe the main objects you see in this image in one sentence.",
                        img
                    ])
                    desc = response.text.strip()
                    descriptions.append(f"Direction {i+1}: {desc}")
                    print(f"  ✓ {desc}")
                except Exception as e:
                    print(f"  ✗ Vision error: {e}")
            
            # Rotate for next photo (except last one)
            if i < num_photos - 1:
                self.turn_right(50, rotation_time)
                time.sleep(0.3)
        
        # Compile and speak summary
        if descriptions:
            summary = "I completed the scan. Here's what I found. " + " ".join(descriptions)
            self.speak(summary)
        else:
            self.speak("I completed the scan but couldn't analyze the images", interruptible=False)
    
    def listen(self):
        """Listen to user with interrupt detection"""
        with sr.Microphone() as source:
            print("\n👂 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=5)
                print("⏳ Processing...")
                text = self.recognizer.recognize_google(audio)
                print(f"👤 You: {text}")
                return text
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                print(f"Listen error: {e}")
                return ""
    
    def capture_image(self, prefix="view"):
        """Capture fresh image"""
        try:
            # Flush buffer
            for _ in range(5):
                self.cap.read()
            
            ret, frame = self.cap.read()
            if ret:
                filename = f"{prefix}_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                return filename
        except Exception as e:
            print(f"Camera error: {e}")
        return None
    
    def what_do_i_see(self):
        """Describe current scene"""
        self.speak("Let me look", interruptible=False)
        img_path = self.capture_image()
        
        if not img_path:
            self.speak("Camera error", interruptible=False)
            return
        
        try:
            img = Image.open(img_path)
            response = self.model.generate_content([
                "Describe what you see in this image in 2-3 sentences.",
                img
            ])
            self.speak(response.text)
        except Exception as e:
            self.speak("Vision error", interruptible=False)
            print(f"Vision error: {e}")
    
    def understand_command(self, command):
        """Use AI to understand ANY variation of commands"""
        prompt = f"""You are a robot command interpreter. Analyze: "{command}"

Determine the user's intent. Respond with ONE of these categories:
MOVEMENT, VISION, SCAN, QUESTION, TEST, INTERRUPT, CONTINUE, EXIT, UNKNOWN

For MOVEMENT, also extract:
- Direction: forward/backward/left/right/stop
- Duration: seconds (default 2 for forward/back, 1 for turns)
- Speed: 40 (slow), 60 (normal), or 80 (fast)

Format:
CATEGORY: [category]
DIRECTION: [if movement]
DURATION: [if movement]
SPEED: [if movement]

Examples:
"go ahead" → CATEGORY: MOVEMENT, DIRECTION: forward, DURATION: 2, SPEED: 60
"what do you see" → CATEGORY: VISION
"scan around" → CATEGORY: SCAN
"stop talking" → CATEGORY: INTERRUPT
"keep going" → CATEGORY: CONTINUE
"what is AI" → CATEGORY: QUESTION
"""
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text
            
            # Parse response
            category = "UNKNOWN"
            direction = "forward"
            duration = 2.0
            speed = 60
            
            # Extract category
            cat_match = re.search(r'CATEGORY:\s*(\w+)', result, re.IGNORECASE)
            if cat_match:
                category = cat_match.group(1).upper()
            
            # Extract movement details
            dir_match = re.search(r'DIRECTION:\s*(\w+)', result, re.IGNORECASE)
            if dir_match:
                direction = dir_match.group(1).lower()
            
            dur_match = re.search(r'DURATION:\s*(\d+\.?\d*)', result, re.IGNORECASE)
            if dur_match:
                duration = float(dur_match.group(1))
            
            spd_match = re.search(r'SPEED:\s*(\d+)', result, re.IGNORECASE)
            if spd_match:
                speed = int(spd_match.group(1))
            
            return category, direction, duration, speed
            
        except Exception as e:
            print(f"Command parsing error: {e}")
            # Default to treating as question
            return "QUESTION", "forward", 2.0, 60
    
    def execute_movement(self, direction, duration, speed):
        """Execute movement command"""
        try:
            if direction == "forward":
                self.speak("Moving forward", interruptible=False)
                self.move_forward(int(speed), duration)
            elif direction == "backward":
                self.speak("Moving backward", interruptible=False)
                self.move_backward(int(speed), duration)
            elif direction == "left":
                self.speak("Turning left", interruptible=False)
                self.turn_left(int(speed), duration)
            elif direction == "right":
                self.speak("Turning right", interruptible=False)
                self.turn_right(int(speed), duration)
            elif direction == "stop":
                self.speak("Stopping", interruptible=False)
                self.stop_motors()
        except Exception as e:
            print(f"Movement error: {e}")
            self.speak("Movement error", interruptible=False)
    
    def answer_question(self, question):
        """Answer general question"""
        self.speak("Let me think", interruptible=False)
        try:
            response = self.model.generate_content(question)
            answer = response.text
            if len(answer) > 500:
                answer = answer[:500] + "..."
            self.speak(answer)
        except Exception as e:
            self.speak("Sorry, I cannot answer that", interruptible=False)
            print(f"AI error: {e}")
    
    def process_command(self, command):
        """Main command processor"""
        if not command:
            return True
        
        command_lower = command.lower()
        
        # Check for immediate interrupt
        if any(word in command_lower for word in ["stop talking", "be quiet", "shut up", "silence", "hush", "quiet"]):
            self.stop_speaking()
            return True
        
        # Check for continue
        if any(word in command_lower for word in ["continue", "keep going", "go on", "proceed", "resume"]):
            self.continue_speaking()
            return True
        
        # Use AI to understand intent
        try:
            category, direction, duration, speed = self.understand_command(command)
            print(f"📊 Understood as: {category}")
            
            if category == "MOVEMENT":
                self.execute_movement(direction, duration, speed)
            
            elif category == "VISION":
                self.what_do_i_see()
            
            elif category == "SCAN":
                self.scan_surroundings()
            
            elif category == "TEST":
                self.test_motor_directions()
            
            elif category == "INTERRUPT":
                self.stop_speaking()
            
            elif category == "CONTINUE":
                self.continue_speaking()
            
            elif category == "EXIT":
                self.speak("Goodbye! Shutting down", interruptible=False)
                return False
            
            elif category == "QUESTION":
                self.answer_question(command)
            
            else:
                # Default to question
                self.answer_question(command)
                
        except Exception as e:
            print(f"Command processing error: {e}")
            self.speak("I didn't understand that", interruptible=False)
        
        return True
    
    def run(self):
        """Main loop"""
        welcome = "Advanced AI Robot ready. I understand natural commands and can scan surroundings. Say help for examples"
        self.speak(welcome, interruptible=False)
        
        running = True
        try:
            while running:
                command = self.listen()
                
                if not command:
                    continue
                
                if "help" in command.lower():
                    help_text = """I understand natural language. Try these examples. 
                    Movement: go forward, reverse, spin right, move ahead slowly. 
                    Vision: what do you see, look around, describe scene. 
                    Scan: scan surroundings, look around 360. 
                    Control: stop talking to interrupt me, continue to resume, test motors. 
                    Questions: Ask me anything. 
                    Say goodbye to exit."""
                    self.speak(help_text)
                else:
                    running = self.process_command(command)
                
                time.sleep(0.3)
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Emergency stop!")
            self.speak("Emergency stop activated", interruptible=False)
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        print("\n🔄 Cleaning up...")
        
        with self.speech_lock:
            self.should_stop_speaking = True
        
        # Stop speech
        pygame.mixer.music.stop()
        
        # Wait for speaking thread
        if self.speaking_thread and self.speaking_thread.is_alive():
            self.speaking_thread.join(timeout=2)
        
        # Stop motors
        self.stop_motors()
        self.pwm_left.stop()
        self.pwm_right.stop()
        
        # Cleanup GPIO
        GPIO.cleanup()
        
        # Release camera
        if self.cap:
            self.cap.release()
        
        # Quit pygame
        pygame.mixer.quit()
        
        # Clean up temp speech files
        try:
            import glob
            for f in glob.glob("speech_*.mp3"):
                try:
                    os.remove(f)
                except:
                    pass
        except:
            pass
        
        print("✅ Robot stopped")

# Main
if __name__ == "__main__":
    print("=" * 70)
    print("      🤖 ADVANCED AI ROBOT - NATURAL LANGUAGE CONTROL")
    print("=" * 70)
    print("\n💡 Features:")
    print("  ✅ Natural language understanding")
    print("  ✅ 360-degree surroundings scan")
    print("  ✅ Interruptible speech (say 'stop talking')")
    print("  ✅ Continue feature (say 'continue')")
    print("  ✅ Fixed motor directions")
    print("  ✅ Vision AI")
    print("  ✅ Thread-safe operation\n")
    
    try:
        with open('config.json', 'r') as f:
            api_key = json.load(f)['gemini_api_key']
    except FileNotFoundError:
        print("❌ ERROR: config.json not found!")
        print("Create it with: {\"gemini_api_key\": \"YOUR_KEY\"}")
        exit()
    except KeyError:
        print("❌ ERROR: 'gemini_api_key' not found in config.json")
        exit()
    except Exception as e:
        print(f"❌ ERROR loading config: {e}")
        exit()
    
    try:
        robot = AdvancedAIRobot(api_key)
        robot.run()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        GPIO.cleanup()