import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for motor control **NEW NUMBERS**
Front_ENA = 19
Front_IN1 = 26
Front_IN2 = 6
Front_IN3 = 5
Front_IN4 = 22
Front_ENB = 13

Back_ENB = 12
Back_IN4 = 16
Back_IN3 = 25
Back_IN2 = 24
Back_IN1 = 23
Back_ENA = 18

# Set up GPIO pins as outputs
GPIO.setup(Front_ENA, GPIO.OUT)
GPIO.setup(Front_IN1, GPIO.OUT)
GPIO.setup(Front_IN2, GPIO.OUT)
GPIO.setup(Front_IN3, GPIO.OUT)
GPIO.setup(Front_IN4, GPIO.OUT)
GPIO.setup(Front_ENB, GPIO.OUT)

GPIO.setup(Back_ENA, GPIO.OUT)
GPIO.setup(Back_IN1, GPIO.OUT)
GPIO.setup(Back_IN2, GPIO.OUT)
GPIO.setup(Back_IN3, GPIO.OUT)
GPIO.setup(Back_IN4, GPIO.OUT)
GPIO.setup(Back_ENB, GPIO.OUT)

# Create PWM objects for controlling the motor speed
Front_pwm_a = GPIO.PWM(Front_ENA, 100)  # 100 Hz frequency
Front_pwm_b = GPIO.PWM(Front_ENB, 100)  # 100 Hz frequency

Back_pwm_a = GPIO.PWM(Back_ENA, 100)  # 100 Hz frequency
Back_pwm_b = GPIO.PWM(Back_ENB, 100)  # 100 Hz frequency

# Start PWM with 0% duty cycle (stopped initially)
Front_pwm_a.start(0)
Front_pwm_b.start(0)

Back_pwm_a.start(0)
Back_pwm_b.start(0)

# Function to control the motors and their speed
def set_motor_speed(Front_speed_a, Front_speed_b, Back_speed_a, Back_speed_b):
    # Set Front motors
    if Front_speed_a >= 0:
        GPIO.output(Front_IN1, GPIO.HIGH)
        GPIO.output(Front_IN2, GPIO.LOW)
    else:
        GPIO.output(Front_IN1, GPIO.LOW)
        GPIO.output(Front_IN2, GPIO.HIGH)
    
    if Front_speed_b >= 0:
        GPIO.output(Front_IN3, GPIO.HIGH)
        GPIO.output(Front_IN4, GPIO.LOW)
    else:
        GPIO.output(Front_IN3, GPIO.LOW)
        GPIO.output(Front_IN4, GPIO.HIGH)
    
    # Set Back motors
    if Back_speed_a >= 0:
        GPIO.output(Back_IN1, GPIO.HIGH)
        GPIO.output(Back_IN2, GPIO.LOW)
    else:
        GPIO.output(Back_IN1, GPIO.LOW)
        GPIO.output(Back_IN2, GPIO.HIGH)
    
    if Back_speed_b >= 0:
        GPIO.output(Back_IN3, GPIO.HIGH)
        GPIO.output(Back_IN4, GPIO.LOW)
    else:
        GPIO.output(Back_IN3, GPIO.LOW)
        GPIO.output(Back_IN4, GPIO.HIGH)
    
    # Set motor speeds
    Front_pwm_a.ChangeDutyCycle(abs(Front_speed_a))
    Front_pwm_b.ChangeDutyCycle(abs(Front_speed_b))
    Back_pwm_a.ChangeDutyCycle(abs(Back_speed_a))
    Back_pwm_b.ChangeDutyCycle(abs(Back_speed_b))


set_motor_speed(3, 3, 3, 3)  # Move forward at 3% speed all motors
time.sleep(20)  # Keep moving for 20 seconds

set_motor_speed(100, 100, 100, 100)  # Move forward at 100% speed all motors
time.sleep(10)  # Keep moving for 10 seconds

set_motor_speed(0, 0, 0, 0)  # Stop
time.sleep(4)  # Stop for 4 seconds

set_motor_speed(-50, -50, -50, -50)  # Move backward at 50% speed all motors
time.sleep(20)  # Keep moving for 20 seconds

# Cleanup GPIO
Front_pwm_a.stop()
Front_pwm_b.stop()
Back_pwm_a.stop()
Back_pwm_b.stop()
GPIO.cleanup()
