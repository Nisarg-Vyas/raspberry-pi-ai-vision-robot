#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           AI Robot System Test Suite                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Helper function
test_component() {
    echo -n "Testing $1... "
    if $2 &> /dev/null; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((FAILED++))
    fi
}

# Change to project directory
cd "$(dirname "$0")/.." || exit

# Activate virtual environment
if [ -d "robot_env" ]; then
    source robot_env/bin/activate
else
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo "Run setup.sh first"
    exit 1
fi

echo "🧪 Running system tests..."
echo ""

# Test 1: Python
test_component "Python Installation" "python --version"

# Test 2: Config file
echo -n "Testing Config File... "
if [ -f "config.json" ]; then
    if grep -q "gemini_api_key" config.json; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠ WARNING: API key not set${NC}"
    fi
else
    echo -e "${RED}✗ FAILED${NC}"
    ((FAILED++))
fi

# Test 3: Camera
echo -n "Testing Camera... "
if [ -e "/dev/video0" ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    ((FAILED++))
fi

# Test 4: GPIO
test_component "GPIO Access" "python -c 'import RPi.GPIO'"

# Test 5: OpenCV
test_component "OpenCV" "python -c 'import cv2'"

# Test 6: Speech Recognition
test_component "Speech Recognition" "python -c 'import speech_recognition'"

# Test 7: gTTS
test_component "Text-to-Speech" "python -c 'from gtts import gTTS'"

# Test 8: Pygame
test_component "Pygame (Audio)" "python -c 'import pygame'"

# Test 9: Gemini API
test_component "Gemini API" "python -c 'import google.generativeai'"

# Test 10: PIL
test_component "Image Processing" "python -c 'from PIL import Image'"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Test Results                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed! Robot is ready.${NC}"
    echo ""
    echo "📋 Next steps:"
    echo "1. Ensure config.json has your Gemini API key"
    echo "2. Connect Bluetooth speaker"
    echo "3. Run: python robot_advanced_fixed.py 2>/dev/null"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Check installation.${NC}"
    echo ""
    echo "Try running setup.sh again:"
    echo "./setup.sh"
    exit 1
fi