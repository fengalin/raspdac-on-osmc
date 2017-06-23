#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO
import dbus, sys

# get active jobs to determine if we are shutting down or rebooting
systemd1 = dbus.SystemBus().get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
job_list = manager.ListJobs()

is_shutting_down = False
is_rebooting = False
for active_job in job_list:
    if active_job[1] == "shutdown.target" and active_job[2] == "start":
        is_shutting_down = True
    elif active_job[1] == "reboot.target" and active_job[2] == "start":
        is_rebooting = True

if is_shutting_down:
    # note: this includes both rebooting and shutting down for powering offf
    GPIO.setmode(GPIO.BCM)

    # raspdac poweroff/reboot commands start by maintaining a HIGH level on GPIO04 (reboot doesn't need anything else)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)
    sleep(1) # maintain the level long enough to be ack by the power manager

    if is_rebooting:
        print("Raspdac rebooting...")
    else:
        # shutdown for poweroff command needs leaving GPIO04 in LOW level
        print("Raspdac powering off...")
        GPIO.output(4, GPIO.LOW)

    # Note: don't GPIO.cleanup() because it would cause a LOW level
    # which would be considered as a poweroff command even for a reboot
# else: probably just reloading the service
