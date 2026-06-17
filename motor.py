import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

ENA = 2
IN1 = 3
IN2 = 4
ENB = 17
IN3 = 22
IN4 = 27

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwmA = GPIO.PWM(ENA, 100)
pwmB = GPIO.PWM(ENB, 100)
pwmA.start(0)
pwmB.start(0)

def move(speed=50, turn=0):
    leftSpeed  = speed - turn
    rightSpeed = speed + turn
    leftSpeed  = max(min(leftSpeed,  100), -100)
    rightSpeed = max(min(rightSpeed, 100), -100)

    if leftSpeed >= 0:
        GPIO.output(IN1, 1)
        GPIO.output(IN2, 0)
    else:
        GPIO.output(IN1, 0)
        GPIO.output(IN2, 1)

    if rightSpeed >= 0:
        GPIO.output(IN3, 1)
        GPIO.output(IN4, 0)
    else:
        GPIO.output(IN3, 0)
        GPIO.output(IN4, 1)

    pwmA.ChangeDutyCycle(abs(leftSpeed))
    pwmB.ChangeDutyCycle(abs(rightSpeed))

def stop():
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)

def cleanup():
    GPIO.cleanup()