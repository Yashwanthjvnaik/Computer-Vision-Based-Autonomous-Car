import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def getDistance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = time.time() + 0.04  # 40ms max (~400cm range)

    start = time.time()
    while GPIO.input(ECHO) == 0:
        start = time.time()
        if time.time() > timeout:
            return -1  # no echo received

    stop = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()
        if time.time() > timeout:
            return -1  # object too far or sensor stuck

    elapsed = stop - start
    distance = (elapsed * 34300) / 2
    return distance