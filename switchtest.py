import time
import RPi.GPIO as GPIO
import sys
import numpy as np
from matplotlib import pyplot as plt
from numpy.random import *

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

t = 10
sw = 0

x_list = []
y_list = []

x_list.append(0)
y_list.append(0)


while True:
    try:
        for i in range(1,100):
            print("6:",GPIO.input(6))
            print("7:",GPIO.input(7))
            print("5:",GPIO.input(5))

            if (GPIO.input(6) + GPIO.input(7) + GPIO.input(5)) >= 2:
                sw = 1

            else:
                sw = 0

            x_list.append(i)
            y_list.append(sw)

            time.sleep(1)

        plt.plot(x_list, y_list, color = "b")
        plt.ylim(0, 2)
        plt.show()

            

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