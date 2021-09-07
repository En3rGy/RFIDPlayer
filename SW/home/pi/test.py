#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

pin_wifi_rd = 5
pin_wifi_gr = 7
pin_rfid_rd = 10
pin_rfid_gr = 12

#############################################

GPIO.setup(pin_wifi_rd, GPIO.OUT)
GPIO.setup(pin_wifi_gr, GPIO.OUT)
GPIO.setup(pin_rfid_rd, GPIO.OUT)
GPIO.setup(pin_rfid_gr, GPIO.OUT)

GPIO.output(pin_wifi_rd, GPIO.HIGH)
GPIO.output(pin_wifi_gr, GPIO.LOW)
GPIO.output(pin_rfid_rd, GPIO.HIGH)
GPIO.output(pin_rfid_gr, GPIO.LOW)

time.sleep(4)

GPIO.output(pin_wifi_rd, GPIO.LOW)
GPIO.output(pin_wifi_gr, GPIO.HIGH)
GPIO.output(pin_rfid_rd, GPIO.LOW)
GPIO.output(pin_rfid_gr, GPIO.HIGH)

time.sleep(4)

GPIO.output(pin_wifi_rd, GPIO.LOW)
GPIO.output(pin_wifi_gr, GPIO.LOW)
GPIO.output(pin_rfid_rd, GPIO.LOW)
GPIO.output(pin_rfid_gr, GPIO.LOW)


#### functions #################################################


GPIO.cleanup()
