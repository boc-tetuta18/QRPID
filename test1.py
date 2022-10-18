import RPi.GPIO as GPIO
import sys

duty = 100

#GPIO initial set
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

p1 = GPIO.PWM(27, 100) #50Hz
p2 = GPIO.PWM(22, 100) #50Hz
            
p1.start(0)
p2.start(0)

try:
    while True:
        #「e」キーが押されたら前進
        c = sys.stdin.read(1)
        if c == 'e':
            p1.ChangeDutyCycle(duty)
            p2.ChangeDutyCycle(0)
              
        #「d」キーが押されたら後退
        if c == 'd':
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(duty)

        #「q」キーが押されたら止まる
        if c == 'q':
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(0)

except KeyboardInterrupt:
    pass

GPIO.cleanup()