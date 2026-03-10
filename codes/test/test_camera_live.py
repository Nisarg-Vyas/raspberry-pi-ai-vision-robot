#!/usr/bin/env python3
"""
Camera Test Script
Captures test photos from webcam
"""

import cv2
import time
import sys

def test_camera():
    print("=" * 60)
    print("           📷 CAMERA TEST SCRIPT")
    print("=" * 60)
    print("\nTesting camera capture...\n")
    
    # Initialize camera
    print("⚙️  Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Cannot open camera!")
        print("\nTroubleshooting:")
        print("1. Check if camera is connected")
        print("2. Run: ls /dev/video*")
        print("3. Try different index: cv2.VideoCapture(1)")
        return False
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("✅ Camera opened successfully!")
    print(f"   Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    print("\n📸 Capturing 3 test photos...\n")
    
    try:
        for i in range(3):
            print(f"Capturing photo {i+1}/3...")
            
            # Flush buffer for fresh image
            for _ in range(5):
                cap.read()
            
            # Capture frame
            ret, frame = cap.read()
            
            if ret:
                filename = f"test_photo_{i+1}.jpg"
                cv2.imwrite(filename, frame)
                print(f"✅ Saved: {filename}")
            else:
                print(f"❌ Failed to capture photo {i+1}")
                return False
            
            time.sleep(2)
        
        print("\n✅ Camera test complete!")
        print("\nCheck your folder for:")
        print("  - test_photo_1.jpg")
        print("  - test_photo_2.jpg")
        print("  - test_photo_3.jpg")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        cap.release()
        print("\n🔄 Camera released")

if __name__ == "__main__":
    success = test_camera()
    sys.exit(0 if success else 1)