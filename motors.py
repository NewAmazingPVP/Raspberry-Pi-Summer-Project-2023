import RPi.GPIO as GPIO
import time
import pygame

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

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
Front_pwm_a = GPIO.PWM(Front_ENA, 100)  
Front_pwm_b = GPIO.PWM(Front_ENB, 100) 

Back_pwm_a = GPIO.PWM(Back_ENA, 100)  # 100 Hz frequency
Back_pwm_b = GPIO.PWM(Back_ENB, 100)  

# Start PWM with 0% duty cycle (stopped initially)
Front_pwm_a.start(0)
Front_pwm_b.start(0)

Back_pwm_a.start(0)
Back_pwm_b.start(0)

# Function to control the motors and their speed for Mecanum wheels
def set_mecanum_speed(front_left, front_right, back_left, back_right):
    if front_left >= 0:
        GPIO.output(Front_IN1, GPIO.HIGH)
        GPIO.output(Front_IN2, GPIO.LOW)
    else:
        GPIO.output(Front_IN1, GPIO.LOW)
        GPIO.output(Front_IN2, GPIO.HIGH)

    if front_right >= 0:
        GPIO.output(Front_IN3, GPIO.HIGH)
        GPIO.output(Front_IN4, GPIO.LOW)
    else:
        GPIO.output(Front_IN3, GPIO.LOW)
        GPIO.output(Front_IN4, GPIO.HIGH)

    # Set Back motors
    if back_left >= 0:
        GPIO.output(Back_IN1, GPIO.HIGH)
        GPIO.output(Back_IN2, GPIO.LOW)
    else:
        GPIO.output(Back_IN1, GPIO.LOW)
        GPIO.output(Back_IN2, GPIO.HIGH)

    if back_right >= 0:
        GPIO.output(Back_IN3, GPIO.HIGH)
        GPIO.output(Back_IN4, GPIO.LOW)
    else:
        GPIO.output(Back_IN3, GPIO.LOW)
        GPIO.output(Back_IN4, GPIO.HIGH)

    # Set motor speeds
    Front_pwm_a.ChangeDutyCycle(abs(front_left))
    Front_pwm_b.ChangeDutyCycle(abs(front_right))
    Back_pwm_a.ChangeDutyCycle(abs(back_left))
    Back_pwm_b.ChangeDutyCycle(abs(back_right))
    

pygame.joystick.init()

pygame.display.init()

try:

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        pygame.event.pump()

        x_value_left = joystick.get_axis(0)
        y_value_left = joystick.get_axis(1)
        
        x_value_right = joystick.get_axis(2)
        y_value_right = joystick.get_axis(3)

        # Scale the axis values to match the motor speed range (-100 to 100) for left stick
        front_left_speed = (y_value_left - x_value_left) * 50
        front_right_speed = (y_value_left + x_value_left) * 50
        back_left_speed = (y_value_left + x_value_left) * 50
        back_right_speed = (y_value_left - x_value_left) * 50

        # Scale the axis values to control the rotation of the car using the right stick
        rotation_speed = x_value_right * 100

        # Calculate the individual motor speeds to achieve rotation
        front_left_rotation = rotation_speed
        front_right_rotation = -rotation_speed
        back_left_rotation = rotation_speed
        back_right_rotation = -rotation_speed

        # Combine the rotation speeds with the left joystick speeds
        front_left_speed += front_left_rotation
        front_right_speed += front_right_rotation
        back_left_speed += back_left_rotation
        back_right_speed += back_right_rotation

        set_mecanum_speed(front_left_speed, front_right_speed, back_left_speed, back_right_speed)

except KeyboardInterrupt:
    pass

finally:
    # Stop the motors and clean up GPIO
    set_mecanum_speed(0, 0, 0, 0)
    Front_pwm_a.stop()
    Front_pwm_b.stop()
    Back_pwm_a.stop()
    Back_pwm_b.stop()
    GPIO.cleanup()


