import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for motor control
ENA = 26
IN1 = 19
IN2 = 13
IN3 = 6
IN4 = 5
ENB = 0

# Set up GPIO pins as outputs
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Create PWM objects for controlling the motor speed
pwm_a = GPIO.PWM(ENA, 100)  # 100 Hz frequency
pwm_b = GPIO.PWM(ENB, 100)  # 100 Hz frequency

# Start PWM with 0% duty cycle (stopped initially)
pwm_a.start(0)
pwm_b.start(0)

# Function to control the motors and their speed
def set_motor_speed(speed_a, speed_b):
    # Set motor A
    if speed_a >= 0:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    
    # Set motor B
    if speed_b >= 0:
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    else:
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    
    # Set motor speeds
    pwm_a.ChangeDutyCycle(abs(speed_a))
    pwm_b.ChangeDutyCycle(abs(speed_b))

# Example usage: move forward for 2 seconds, then stop for 1 second, then move backward for 2 seconds

set_motor_speed(3, 3)  # Move forward at 50% speed
time.sleep(20)  # Keep moving for 2 seconds

set_motor_speed(100, 100)  # Move forward at 50% speed
time.sleep(10)  # Keep moving for 2 seconds

set_motor_speed(0, 0)  # Stop
time.sleep(4)  # Stop for 1 second

set_motor_speed(-50, -50)  # Move backward at 50% speed
time.sleep(20)  # Keep moving for 2 seconds

# Cleanup GPIO
pwm_a.stop()
pwm_b.stop()
GPIO.cleanup()
