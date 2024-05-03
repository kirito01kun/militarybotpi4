import RPi.GPIO as GPIO
import time
from mpu import read_accel
import stable

# Define GPIO pins 
IN1 = 5
IN2 = 6
IN3 = 13
IN4 = 19
IN5 = 23
IN6 = 24
IN7 = 12
IN8 = 16
SERVO_PIN = 18

def get_mpu():
    if read_accel() > 0:
        stable.STABLE = 1
    else:
        stable.STABLE = -1

# Initialize GPIO
def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(IN5, GPIO.OUT)
    GPIO.setup(IN6, GPIO.OUT)
    GPIO.setup(IN7, GPIO.OUT)
    GPIO.setup(IN8, GPIO.OUT)
    GPIO.setup(SERVO_PIN, GPIO.OUT)


def forward(duration=.7):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(IN5, GPIO.LOW)
    GPIO.output(IN6, GPIO.HIGH)
    GPIO.output(IN7, GPIO.LOW)
    GPIO.output(IN8, GPIO.HIGH)
    time.sleep(duration)
    stop()


def backward(duration=.7):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(IN5, GPIO.HIGH)
    GPIO.output(IN6, GPIO.LOW)
    GPIO.output(IN7, GPIO.HIGH)
    GPIO.output(IN8, GPIO.LOW)
    time.sleep(duration)
    stop()

def left(duration=.3):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(IN5, GPIO.HIGH)
    GPIO.output(IN6, GPIO.LOW)
    GPIO.output(IN7, GPIO.HIGH)
    GPIO.output(IN8, GPIO.LOW)
    
    time.sleep(duration)
    stop()


def right(duration=.3):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(IN5, GPIO.LOW)
    GPIO.output(IN6, GPIO.HIGH)
    GPIO.output(IN7, GPIO.LOW)
    GPIO.output(IN8, GPIO.HIGH)
    time.sleep(duration)
    stop()

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(IN5, GPIO.LOW)
    GPIO.output(IN6, GPIO.LOW)
    GPIO.output(IN7, GPIO.LOW)
    GPIO.output(IN8, GPIO.LOW)

def servo(dir):
    angle = 90
    if(dir == 'cd'):
        angle = 70
    elif(dir == 'cu'):
        angle = 110
    else:
        angle = 90

    if(dir == 'cd' or dir == 'cu' or dir == 'c'):
        pwm = GPIO.PWM(SERVO_PIN, 50)
        pwm.start(0)
        duty_cycle = angle / 18 + 2
        GPIO.output(SERVO_PIN, True)
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.3)
        pwm.stop()

# Cleanup GPIO
def cleanup():
    GPIO.cleanup()

def handle(cmd):
    try:
        get_mpu()
        if(stable.STABLE > 0):
            print("Stable: ", stable.STABLE)
            setup_gpio()
            if(cmd == 'u'):
                forward()
            elif(cmd == 'ul'):
                forward(3.0)
            elif(cmd == 'b'):
                backward()
            elif(cmd == 'bl'):
                backward(3.0)
            elif(cmd == 'r'):
                right()
                print("right")
            elif(cmd == 'rl'):
                right(1.0)
            elif(cmd == 'l'):
                left()
                print("left")
            elif(cmd == 'lel'):
                left(1.0)
            else:
                servo(cmd)
        else:
            print("STABLE: ", stable.STABLE)
            setup_gpio()
            if(cmd == 'u'):
                backward()
            elif(cmd == 'ul'):
                backward(3.0)
            elif(cmd == 'b'):
                forward()
            elif(cmd == 'bl'):
                forward(3.0)
            elif(cmd == 'r'):
                right()
                print("left")
            elif(cmd == 'rl'):
                right(1.0)
            elif(cmd == 'l'):
                left()
                print("right")
            elif(cmd == 'lel'):
                left(1.0)
            else:
                servo(cmd)
    finally:
        stop()
        cleanup()


# Main function to test motor movements
def main():
    try:
        while(True):
            ui = input('what ?')
            handle(ui)

    finally:
        stop()
        cleanup()

if __name__ == "__main__":
    main()
