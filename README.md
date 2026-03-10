# 🤖 Advanced AI-Powered Voice-Controlled Robot

An intelligent robot built with Raspberry Pi that combines computer vision, natural language processing, and autonomous navigation using Google's Gemini AI.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red.svg)

## ✨ Features

- 🗣️ **Natural Language Understanding** - Understands commands in ANY phrasing (no hardcoded phrases)
- 👁️ **Computer Vision** - AI-powered scene description and object recognition
- 🔄 **360° Environmental Scan** - Rotates and captures surroundings with AI analysis
- ⏸️ **Interruptible Speech** - Say "stop talking" to interrupt, "continue" to resume
- 🚗 **Smart Motor Control** - Four-wheel drive with PWM speed control
- 🎯 **Intent Recognition** - AI parses direction, speed, and duration from natural commands

## 📹 Demo

[Add your demo video/GIF here]

## 🛠️ Hardware Components

### Required:
- Raspberry Pi 4B (2GB+ RAM recommended)
- USB Webcam
- Bluetooth Speaker with Microphone
- L298N Motor Driver
- 4x DC Motors with wheels
- Motor chassis
- Power supplies:
  - 5V 3A for Raspberry Pi
  - 7-12V battery pack for motors

### Optional (for future enhancements):
- HC-SR04 Ultrasonic Sensor
- 128x64 I2C OLED Display (SSD1306)
- USB/Bluetooth Game Controller

## 🔌 Wiring Diagram
```
L298N Motor Driver → Raspberry Pi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENA (Left PWM)  → GPIO 17
IN1 (Left Dir)  → GPIO 27
IN2 (Left Dir)  → GPIO 22
IN3 (Right Dir) → GPIO 23
IN4 (Right Dir) → GPIO 24
ENB (Right PWM) → GPIO 18
GND             → GND (common ground)

Motor Connections:
OUT1 & OUT2 → Both left motors (parallel)
OUT3 & OUT4 → Both right motors (parallel)
```

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-robot.git
cd ai-robot
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Configure API Key
Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
```bash
cp config.json.example config.json
nano config.json
```

Add your API key:
```json
{
    "gemini_api_key": "YOUR_API_KEY_HERE"
}
```

### 4. Connect Bluetooth Speaker
```bash
bluetoothctl
scan on
pair XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
exit
```

### 5. Test Components
```bash
./quick_test.sh
```

## 🧪 Testing Your Setup

After installation, test each component individually:

### Quick Test All Components
```bash
cd ~/robot_project
source robot_env/bin/activate
./tests/quick_test.sh
```

### Individual Component Tests

#### Test Motors
```bash
python tests/test_motors.py
```
Expected: Robot moves forward, backward, left, right

**If robot turns in circles instead of going forward:**
```bash
python tests/fix_motors.py
```
This diagnostic will find the correct motor configuration.

#### Test Camera
```bash
python tests/test_camera.py
```
Expected: Creates 3 test photos (test_photo_1.jpg, test_photo_2.jpg, test_photo_3.jpg)

#### Test Speaker
```bash
python tests/test_speaker.py
```
Expected: Hear 4 spoken phrases

#### Test Microphone
```bash
python tests/test_microphone.py
```
Expected: Robot recognizes your speech (2 out of 3 tests should pass)

**Tip:** Speak clearly and loudly for best results

#### Test Gemini AI (Text)
```bash
python tests/test_gemini.py
```
Expected: AI answers 3 questions

#### Test Gemini Vision
```bash
python tests/test_gemini_vision.py
```
Expected: AI describes what camera sees

#### Test Ultrasonic Sensor (if installed)
```bash
python tests/test_ultrasonic.py
```
Expected: Shows distance measurements as you move your hand

#### Check Available AI Models
```bash
python tests/check_models.py
```
Lists all Gemini models available for your API key

#### Test Different Voices (Optional)
```bash
python tests/test_voices.py
```
Tests different TTS voices to find the best one

---

### Troubleshooting Test Failures

| Test Failed | Solution |
|-------------|----------|
| Motors turn in circles | Run `python tests/fix_motors.py` |
| Camera not working | Check `ls /dev/video*`, try USB port |
| Speaker no sound | Check Bluetooth connection with `bluetoothctl` |
| Mic not hearing | Speak louder, check internet connection |
| Gemini API error | Verify API key in config.json |
| Ultrasonic out of range | Check voltage divider circuit |

For detailed troubleshooting, see [TROUBLESHOOTING.md](docs/troubleshooting.md)

## 🚀 Usage

### Start the Robot
```bash
source robot_env/bin/activate
python robot_advanced_fixed.py 2>/dev/null
```

### Voice Commands

#### Movement
- "Go forward"
- "Move backward slowly"
- "Turn left"
- "Spin right fast"
- "Move ahead for 5 seconds"

#### Vision
- "What do you see?"
- "Describe the scene"
- "Look around"

#### 360° Scan
- "Scan surroundings"
- "Look around completely"
- "Show me everything"

#### Interruption & Continue
- "Stop talking" (interrupts speech)
- "Continue" (resumes from where stopped)

#### Testing
- "Test motors"

#### Questions
- "What is artificial intelligence?"
- "Calculate 25 times 4"
- "Tell me a joke"

#### Exit
- "Goodbye" or "Shut down"

## 🧪 Testing Tools

The repository includes comprehensive testing tools:

- `test_motors.py` - Verify motor movements
- `test_camera.py` - Test webcam capture
- `test_speaker.py` - Audio output test
- `test_microphone.py` - Audio input test
- `test_gemini.py` - AI text responses
- `test_gemini_vision.py` - AI vision capabilities
- `fix_motors.py` - Diagnose motor direction issues
- `check_models.py` - List available Gemini models
- `quick_test.sh` - Run all tests at once

Run individual tests:
```bash
python test_motors.py
python test_camera.py
```

## 🏗️ Project Structure
```
ai-robot/
├── robot_advanced_fixed.py       # Main robot program ⭐
├── config.json                   # API keys (create from example)
├── config.json.example           # API key template
├── setup.sh                      # Installation script
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── README.md                     # This file
├── CONTRIBUTING.md               # Contribution guidelines
│
├── tests/                        # Testing utilities
│   ├── test_motors.py           # Test motor movements
│   ├── test_camera.py           # Test webcam capture
│   ├── test_speaker.py          # Test audio output
│   ├── test_microphone.py       # Test audio input
│   ├── test_gemini.py           # Test AI text responses
│   ├── test_gemini_vision.py    # Test AI vision
│   ├── test_ultrasonic.py       # Test distance sensor
│   ├── test_voices.py           # Test different TTS voices
│   ├── fix_motors.py            # Motor direction diagnostic
│   ├── check_models.py          # List available AI models
│   └── quick_test.sh            # Run all tests
│
└── docs/                         # Documentation
    ├── HARDWARE_GUIDE.md        # Hardware setup guide
    ├── TROUBLESHOOTING.md       # Troubleshooting guide
    └── API_SETUP.md             # API configuration guide
```

## 🔧 Troubleshooting

### Robot turns in circles instead of moving forward
```bash
python tests/fix_motors.py
```
Follow the on-screen instructions to find the correct motor configuration.

### Camera shows old images
The code automatically flushes the camera buffer. If issues persist, increase the flush count in `capture_image()`.

### "Stop talking" doesn't work
Lower the microphone energy threshold:
```python
self.recognizer.energy_threshold = 3000  # More sensitive
```

### Motors moving wrong direction
See `docs/TROUBLESHOOTING.md` for detailed motor wiring fixes.

For more issues, see [TROUBLESHOOTING.md](docs/troubleshooting.md)

## 🎯 How It Works

### 1. Natural Language Processing
```python
# AI understands ANY phrasing variation
"go forward" → ACTION: forward, SPEED: 60%, DURATION: 2s
"move ahead slowly" → ACTION: forward, SPEED: 40%, DURATION: 2s
"drive straight fast for 5 seconds" → ACTION: forward, SPEED: 80%, DURATION: 5s
```

### 2. Computer Vision
- Camera captures fresh image (buffer flushed)
- Image sent to Gemini Vision API
- AI describes objects, colors, and scene
- Response spoken aloud

### 3. 360° Scanning
- Robot rotates 360° in 8 increments (45° each)
- Captures and analyzes photo at each position
- Compiles comprehensive environmental description

### 4. Thread-Safe Interruption
- Speech runs in background thread
- Main thread monitors for "stop talking" command
- Thread-safe locks prevent race conditions
- Resume capability tracks sentence position

## 🚧 Future Enhancements

- [ ] Obstacle avoidance with ultrasonic sensor
- [ ] OLED display for status information
- [ ] Manual control with game controller
- [ ] Object tracking and following
- [ ] Face recognition
- [ ] SLAM mapping
- [ ] Gesture control
- [ ] Web interface for remote control

## 📊 Performance

- Voice Command Response: ~2-3 seconds
- Vision Processing: ~3-5 seconds
- 360° Scan Duration: ~30 seconds
- Motor Response: Instant
- Speech Generation: ~1-2 seconds per sentence

## 🔐 API Keys & Security

This project uses Google Gemini API (free tier available):
- Get your key: https://makersuite.google.com/app/apikey
- Free tier: 15 requests/minute
- **Never commit `config.json` to GitHub**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👏 Acknowledgments

- [Google Gemini API](https://ai.google.dev/) for AI capabilities
- [Raspberry Pi Foundation](https://www.raspberrypi.org/)
- [OpenCV](https://opencv.org/) community
- Python speech recognition libraries

## ⭐ Star History

If you find this project helpful, please consider giving it a star!

---

**Built with ❤️ using Raspberry Pi and AI**
