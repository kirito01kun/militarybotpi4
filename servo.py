import RPi.GPIO as GPIO
import time

# Define GPIO pin for Servo Motor
SERVO_PIN = 18

# Initialize GPIO
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

# Function to rotate servo motor to a given angle
def rotate_servo(angle):
    pwm = GPIO.PWM(SERVO_PIN, 50)  # PWM frequency: 50Hz
    pwm.start(0)
    duty_cycle = angle / 18 + 2  # Convert angle to duty cycle
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)  # Adjust this delay as needed for your servo
    pwm.stop()

# Cleanup GPIO
def cleanup():
    GPIO.cleanup()

# Main function to test servo rotation
def main():
    try:
        setup_gpio()
        while True:
            angle = float(input("Enter angle (0-180): "))
            if angle < 0 or angle > 180:
                print("Angle must be between 0 and 180 degrees.")
                continue
            rotate_servo(angle)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()

