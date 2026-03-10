#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       AI Robot Installation Script                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install system dependencies
echo ""
echo "📦 Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    portaudio19-dev \
    python3-pyaudio \
    espeak \
    pulseaudio \
    python3-opencv \
    i2c-tools \
    git \
    ffmpeg

# Enable I2C (for future OLED display)
echo ""
echo "🔧 Enabling I2C..."
sudo raspi-config nonint do_i2c 0

# Create virtual environment
echo ""
echo "🐍 Creating Python virtual environment..."
python3 -m venv robot_env

# Activate virtual environment
echo ""
echo "✅ Activating virtual environment..."
source robot_env/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python packages
echo ""
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Create config file if it doesn't exist
if [ ! -f config.json ]; then
    echo ""
    echo "📝 Creating config.json from template..."
    cp config.json.example config.json
    echo "⚠️  IMPORTANT: Edit config.json and add your Gemini API key!"
fi

# Make test scripts executable
echo ""
echo "🔧 Making test scripts executable..."
chmod +x tests/*.sh 2>/dev/null || true

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p captured_images
mkdir -p logs

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║            Installation Complete! ✅                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1️⃣  Get your free Gemini API key:"
echo "   https://makersuite.google.com/app/apikey"
echo ""
echo "2️⃣  Edit config.json and add your API key:"
echo "   nano config.json"
echo ""
echo "3️⃣  Connect your Bluetooth speaker:"
echo "   bluetoothctl"
echo ""
echo "4️⃣  Test your setup:"
echo "   source robot_env/bin/activate"
echo "   ./tests/quick_test.sh"
echo ""
echo "5️⃣  Run the robot:"
echo "   python robot_advanced_fixed.py 2>/dev/null"
echo ""
echo "📖 For detailed instructions, see README.md"
echo ""