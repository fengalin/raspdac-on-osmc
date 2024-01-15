#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)

sleep(3) # s

print("Raspdac: Waiting for button event")

try:
    channel = GPIO.wait_for_edge(17, GPIO.RISING) # , timeout=5000
    if channel is not None:
        print("Raspdac: Button triggered")
        GPIO.output(22, GPIO.LOW)

        subprocess.call(["sudo", "systemctl", "poweroff"])
    else:
        # timeout
        print("Raspdac: Time out waiting for button")
except:
    print("Raspdac: Exception waiting for button")

GPIO.cleanup()

