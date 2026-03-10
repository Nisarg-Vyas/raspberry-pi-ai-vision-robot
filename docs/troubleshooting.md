# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Problem: `pip install` fails
```bash
# Solution 1: Update pip
pip install --upgrade pip

# Solution 2: Install system dependencies first
sudo apt install python3-dev portaudio19-dev

# Solution 3: Install packages one by one
pip install google-generativeai
pip install RPi.GPIO
# etc...
```

#### Problem: Virtual environment won't activate
```bash
# Solution: Use full path
source ~/robot_project/robot_env/bin/activate

# Or recreate environment
rm -rf robot_env
python3 -m venv robot_env
source robot_env/bin/activate
pip install -r requirements.txt
```

---

### Motor Issues

#### Problem: Robot turns in circles instead of moving forward

**Diagnosis:** Motors are paired by position (front/back) instead of side (left/right)

**Solution 1: Run diagnostic tool**
```bash
python tests/fix_motors.py
```
Follow the prompts. It will test 4 configurations and tell you which one works.

**Solution 2: Fix wiring**
Reconnect motors so:
- OUT1 & OUT2 → Both LEFT motors
- OUT3 & OUT4 → Both RIGHT motors

**Solution 3: Fix code**
Update `robot_advanced_fixed.py` in `move_forward()` function based on diagnostic results.

---

#### Problem: Robot goes backward when commanded forward

**Solution: Swap motor direction in code**

In `robot_advanced_fixed.py`, find `move_forward()` and change:
```python
# From:
GPIO.output(self.IN1, GPIO.HIGH)
GPIO.output(self.IN2, GPIO.LOW)
GPIO.output(self.IN3, GPIO.HIGH)
GPIO.output(self.IN4, GPIO.LOW)

# To:
GPIO.output(self.IN1, GPIO.LOW)
GPIO.output(self.IN2, GPIO.HIGH)
GPIO.output(self.IN3, GPIO.LOW)
GPIO.output(self.IN4, GPIO.HIGH)
```

---

#### Problem: Left and right turns are swapped

**Solution: Swap IN3 and IN4 in code**
Or physically swap the right motor wires on L298N.

---

#### Problem: One side moves faster than the other

**Solution: Adjust PWM duty cycle**

In movement functions, use different speeds:
```python
def move_forward(self, speed=60, duration=2):
    # Adjust these values to balance
    self.pwm_left.ChangeDutyCycle(speed - 5)  # Left slower
    self.pwm_right.ChangeDutyCycle(speed)     # Right normal
```

---

#### Problem: Motors don't move at all

**Check:**
1. Battery voltage (should be 7-12V)
```bash
# Measure with multimeter
```

2. Common ground connection
```bash
# Verify Pi GND connected to L298N GND
```

3. GPIO wiring
```bash
gpio readall  # Check pin assignments
```

4. Test with simple script:
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
pwm = GPIO.PWM(17, 100)
pwm.start(50)
# Should see motor moving
```

---

### Camera Issues

#### Problem: "Cannot open camera" error

**Solution 1: Check camera detection**
```bash
ls /dev/video*
# Should show /dev/video0
```

**Solution 2: Test with system command**
```bash
# For USB webcam
fswebcam test.jpg

# For Pi Camera
raspistill -o test.jpg
```

**Solution 3: Check permissions**
```bash
sudo usermod -a -G video $USER
# Logout and login again
```

**Solution 4: Try different camera index**
In `robot_advanced_fixed.py`:
```python
self.cap = cv2.VideoCapture(0)  # Try 0, 1, 2, etc.
```

---

#### Problem: Camera shows old/cached images

**Solution:** Code already flushes buffer. If issue persists:
```python
# In capture_image(), increase flush count:
for _ in range(10):  # Was 5, now 10
    self.cap.read()
```

---

### Audio Issues

#### Problem: No sound from speaker

**Check:**
1. Bluetooth connection
```bash
bluetoothctl
devices
info XX:XX:XX:XX:XX:XX
# Should show "Connected: yes"
```

2. Volume levels
```bash
alsamixer
# Use arrow keys to adjust
```

3. Audio output device
```bash
aplay -l  # List playback devices
```

**Solution: Reconnect Bluetooth**
```bash
bluetoothctl
disconnect XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
exit
```

---

#### Problem: Microphone not picking up voice

**Check:**
1. Microphone not muted on speaker
2. Input device detected
```bash
arecord -l  # List recording devices
```

**Solution 1: Adjust energy threshold**
In `robot_advanced_fixed.py`:
```python
self.recognizer.energy_threshold = 3000  # Lower = more sensitive
```

**Solution 2: Test microphone**
```bash
python tests/test_microphone.py
```

**Solution 3: Speak louder and closer**

---

#### Problem: ALSA warnings flooding console

**Solution: Redirect stderr**
```bash
python robot_advanced_fixed.py 2>/dev/null
```

These are warnings, not errors. Robot still works.

---

### AI/API Issues

#### Problem: "API key error" or "404 model not found"

**Solution 1: Check API key in config.json**
```bash
nano config.json
# Verify key starts with "AIzaSy..."
```

**Solution 2: Get new API key**
https://makersuite.google.com/app/apikey

**Solution 3: Check model name**
```bash
python tests/check_models.py
# Use one of the listed models
```

---

#### Problem: "Rate limit exceeded"

**Cause:** Free tier limited to 15 requests/minute

**Solution:**
- Wait 1 minute
- Reduce frequency of commands
- Upgrade to paid tier

---

#### Problem: "No internet connection" errors

**Check:**
```bash
ping google.com
# Should see responses
```

**Both Google Speech Recognition and Gemini AI require internet!**

---

### Speech Interruption Issues

#### Problem: "Stop talking" doesn't stop robot

**Solution 1: Increase microphone sensitivity**
```python
self.recognizer.energy_threshold = 2500  # More sensitive
```

**Solution 2: Say louder and clearer**

**Solution 3: Check if speech thread is working**
```python
# Add debug print in stop_speaking():
print(f"is_speaking: {self.is_speaking}")
```

---

#### Problem: "Continue" doesn't resume

**Check:** Was robot interrupted mid-speech?
- If robot finished speaking naturally, nothing to continue
- Only works if interrupted with "stop talking"

---

### 360° Scan Issues

#### Problem: Scan doesn't complete full rotation

**Check rotation time calibration:**
```python
# In scan_surroundings():
rotation_time = 0.5  # Adjust this

# Test with:
# 0.3 = ~35°
# 0.5 = ~45°
# 0.7 = ~55°
```

**Solution: Calibrate for your robot**
1. Say "turn right"
2. Measure actual rotation angle
3. Adjust `rotation_time` proportionally

---

#### Problem: Scan crashes or freezes

**Check:**
1. Internet connection (needs AI API)
2. Camera working (test with `test_camera.py`)
3. Sufficient lighting
4. No API rate limits

---

### Performance Issues

#### Problem: Robot very slow to respond

**Causes:**
1. Slow internet connection
2. API rate limiting
3. Raspberry Pi model (need 4B minimum)
4. Too many background processes

**Solutions:**
```bash
# Check internet speed
speedtest-cli

# Check CPU usage
top

# Upgrade Raspberry Pi model if using Pi 3 or lower
```

---

#### Problem: Speech generation takes too long

**Solution: Shorten responses**
In `robot_advanced_fixed.py`:
```python
if len(answer) > 500:
    answer = answer[:500] + "..."  # Reduce from 500 to 200
```

---

### GPIO/Permission Issues

#### Problem: "Permission denied" GPIO errors

**Solution:**
```bash
sudo usermod -a -G gpio $USER
# Logout and login

# Or run with sudo (not recommended)
sudo python robot_advanced_fixed.py
```

---

#### Problem: GPIO cleanup warnings

**These are usually harmless.** But if persistent:
```python
# In robot code, ensure cleanup:
GPIO.cleanup()

# Or specify pins:
GPIO.cleanup([17, 18, 22, 23, 24, 27])
```

---

### File/Directory Issues

#### Problem: "config.json not found"

**Solution:**
```bash
cp config.json.example config.json
nano config.json
# Add your API key
```

---

#### Problem: Too many image files

**Solution: Auto-cleanup**
```python
# Already implemented in code, but you can adjust:
import glob
images = sorted(glob.glob("view_*.jpg"))
if len(images) > 3:  # Keep only 3 latest
    for img in images[:-3]:
        os.remove(img)
```

---

## Emergency Procedures

### Robot won't stop
1. Press `Ctrl+C` in terminal
2. If frozen, close terminal window
3. As last resort: `sudo reboot`

### GPIO pins stuck HIGH
```bash
# Reset all GPIO
gpio unexportall

# Or reboot
sudo reboot
```

### Complete reset
```bash
# Stop all Python processes
killall python
killall python3

# Cleanup GPIO
python -c "import RPi.GPIO as GPIO; GPIO.cleanup()"

# Reboot
sudo reboot
```

---

## Getting More Help

### Check logs
```bash
# Run with verbose output
python robot_advanced_fixed.py

# Or save to log
python robot_advanced_fixed.py 2>&1 | tee robot.log
```

### Enable debug mode
In `robot_advanced_fixed.py`, add at top:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Report Issues
If problem persists:
1. Check [GitHub Issues](https://github.com/yourusername/ai-robot/issues)
2. Create new issue with:
   - Raspberry Pi model
   - Python version (`python --version`)
   - Error message
   - Steps to reproduce

---

## Preventive Maintenance

### Weekly
- Clean camera lens
- Check wire connections
- Test battery voltage
- Update software

### Monthly
- Backup config.json
- Update system packages
```bash
sudo apt update && sudo apt upgrade
```
- Clean dust from motors
- Tighten screws

---

For hardware-specific issues, see [hardware_guide.md](hardware_guide.md)
