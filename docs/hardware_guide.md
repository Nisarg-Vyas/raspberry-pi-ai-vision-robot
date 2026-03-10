# 🔌 Hardware Setup Guide

## Complete Wiring Diagram

### L298N Motor Driver Connections
```
L298N Pin          →    Connection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENA (Enable A)     →    GPIO 17 (PWM for left motors)
IN1                →    GPIO 27
IN2                →    GPIO 22
IN3                →    GPIO 23
IN4                →    GPIO 24
ENB (Enable B)     →    GPIO 18 (PWM for right motors)
GND                →    Raspberry Pi GND (common ground)
+12V               →    Motor battery positive (7-12V)
+5V                →    NOT CONNECTED (optional: Pi 5V if no battery)

Motor Outputs:
OUT1 & OUT2        →    Both LEFT motors in parallel
OUT3 & OUT4        →    Both RIGHT motors in parallel
```

### Motor Pairing Configuration

**IMPORTANT:** Connect motors by SIDE, not by position!
```
Correct Configuration:
     FRONT
  [L1]  [R1]     L1 = Left Front Motor
  [L2]  [R2]     L2 = Left Rear Motor
     BACK        R1 = Right Front Motor
                 R2 = Right Rear Motor

Wiring:
L1 (+) ──┐
L2 (+) ──┴──→ L298N OUT1
L1 (-) ──┐
L2 (-) ──┴──→ L298N OUT2

R1 (+) ──┐
R2 (+) ──┴──→ L298N OUT3
R1 (-) ──┐
R2 (-) ──┴──→ L298N OUT4
```

**WRONG Configuration (Don't do this!):**
```
❌ OUT1&2 → Front motors
❌ OUT3&4 → Rear motors
This will make the robot turn instead of going straight!
```

### Ultrasonic Sensor (HC-SR04) - Optional

**⚠️ IMPORTANT:** Requires voltage divider for ECHO pin!
```
HC-SR04            Raspberry Pi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VCC           →    5V
GND           →    GND
TRIG          →    GPIO 16
ECHO          →    Voltage Divider → GPIO 12

Voltage Divider Circuit (REQUIRED):
ECHO pin → 1kΩ resistor → GPIO 12
                        ↓
                    2kΩ resistor
                        ↓
                       GND

Why? HC-SR04 outputs 5V but Pi GPIO is 3.3V max!
```

### OLED Display (128x64 I2C SSD1306) - Optional
```
OLED Pin      Raspberry Pi
━━━━━━━━━━━━━━━━━━━━━━━━━━
VCC      →    3.3V (NOT 5V!)
GND      →    GND
SDA      →    GPIO 2 (I2C SDA)
SCL      →    GPIO 3 (I2C SCL)
```

## Power Supply Guide

### Option 1: Dual Power Supply (Recommended)
```
Power Distribution:
┌─────────────────┐
│  5V 3A Supply   │──→ Raspberry Pi (USB-C)
└─────────────────┘

┌─────────────────┐
│  7-12V Battery  │──→ L298N +12V
│     Pack        │──→ GND (common with Pi)
└─────────────────┘
```

### Option 2: Single Battery with Regulator
```
┌──────────────────┐
│  12V Battery     │──┬→ L298N +12V
│      Pack        │  │
└──────────────────┘  │
                      ├→ 5V Regulator → Pi
                      └→ Common GND
```

**Power Consumption:**
- Raspberry Pi: ~5W (1A @ 5V)
- 4 Motors: ~10-15W (varies by load)
- Total: ~15-20W

## Component Shopping List

### Essential Components
| Component | Quantity | Est. Price (₹) |
|-----------|----------|----------------|
| Raspberry Pi 4B (2GB+) | 1 | 3000-4000 |
| USB Webcam | 1 | 500-1000 |
| Bluetooth Speaker w/ Mic | 1 | 800-1500 |
| L298N Motor Driver | 1 | 150-250 |
| DC Motors with Wheels | 4 | 400-600 |
| Robot Chassis | 1 | 300-500 |
| 7-12V Battery Pack | 1 | 400-600 |
| 5V 3A Power Supply | 1 | 300-500 |
| Jumper Wires (M-M, M-F) | 1 set | 100-150 |
| Breadboard | 1 | 50-100 |

**Total: ₹6000-9000**

### Optional Components
| Component | Quantity | Est. Price (₹) |
|-----------|----------|----------------|
| HC-SR04 Ultrasonic | 1 | 50-100 |
| 128x64 OLED Display | 1 | 200-300 |
| Resistors (1kΩ, 2kΩ) | 2 | 10-20 |
| USB Game Controller | 1 | 300-500 |
| Power Bank 5V 3A | 1 | 500-1000 |

## Assembly Instructions

### Step 1: Mount Components on Chassis
1. Attach 4 motors to chassis corners
2. Mount Raspberry Pi on top deck
3. Mount L298N motor driver nearby
4. Mount battery pack underneath

### Step 2: Wire Motors
1. Connect left motors in parallel → OUT1 & OUT2
2. Connect right motors in parallel → OUT3 & OUT4
3. Test polarity: both left motors should spin same direction

### Step 3: Connect L298N to Pi
1. Wire GPIO pins as per diagram
2. Connect common ground (ESSENTIAL!)
3. Power L298N from battery

### Step 4: Connect Peripherals
1. Plug in USB webcam
2. Pair Bluetooth speaker
3. Optional: Wire ultrasonic sensor with voltage divider
4. Optional: Connect OLED display via I2C

### Step 5: Power Up
1. Power on battery pack
2. Power on Raspberry Pi
3. System should boot without errors

## Testing Hardware

### Quick Hardware Check
```bash
# Check GPIO
gpio readall

# Check camera
ls /dev/video*

# Check I2C (for OLED)
sudo i2cdetect -y 1

# Check Bluetooth
bluetoothctl devices
```

### Motor Test
```bash
python tests/test_motors.py
```
Should see: Forward → Backward → Left → Right

### Camera Test
```bash
python tests/test_camera.py
```
Should create 3 test photos

### Audio Test
```bash
python tests/test_speaker.py
python tests/test_microphone.py
```

## Troubleshooting Hardware Issues

### Motors don't move
- Check battery voltage (7-12V)
- Verify common ground connection
- Test with `test_motors.py`
- Check GPIO wiring

### Robot turns instead of going forward
- Motors paired incorrectly (by position instead of side)
- Run `fix_motors.py` diagnostic
- Re-check motor connections to L298N

### One side moves faster
- Motors may have different characteristics
- Adjust PWM values in code:
```python
self.pwm_left.ChangeDutyCycle(55)  # Slower
self.pwm_right.ChangeDutyCycle(60) # Faster
```

### Camera not detected
```bash
# Check connection
ls /dev/video*

# Should show /dev/video0

# Test with system tool
raspistill -o test.jpg  # For Pi Camera
```

### Bluetooth speaker won't connect
```bash
bluetoothctl
power on
scan on
# Find MAC address
pair XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
exit
```

## Safety Warnings

⚠️ **IMPORTANT SAFETY NOTES:**

1. **Never connect 5V to 3.3V GPIO pins** - Will damage Pi!
2. **Always use voltage divider for ECHO pin** on ultrasonic sensor
3. **Common ground is essential** - Connect Pi GND to motor GND
4. **Don't overdraw from Pi** - Use separate power for motors
5. **Check polarity** - Reverse polarity can damage components
6. **Secure connections** - Loose wires can short circuit

## Recommended Tools

- Multimeter (for voltage/continuity testing)
- Wire strippers
- Soldering iron (for permanent connections)
- Heat shrink tubing
- Cable ties
- Screwdrivers (Phillips & flat)
- Hot glue gun (for securing components)

---

For software setup, see [README.md](../README.md)