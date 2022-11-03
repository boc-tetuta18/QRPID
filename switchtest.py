import time
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    try:
        print(GPIO.input(6))
        time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
    """
    if sw_status == 0:
        print('swON')
    else:
        print('a')

    time.sleep(0.3)
    """