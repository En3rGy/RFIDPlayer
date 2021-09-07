#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("Halten Sie ein Clip oder eine Karte an dem Sensor.")

try:
    id, text = reader.read()
    print(id)
    print(text)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
