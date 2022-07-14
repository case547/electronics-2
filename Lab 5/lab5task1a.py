import pyb
from pyb import Pin, Timer

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP)  # control motor A direction
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1')            # control motor A speed

B1 = Pin('X7', Pin.OUT_PP)
B2 = Pin('X8', Pin.OUT_PP)
PWMB = Pin('X2')

# Configure timer 2 to produce 1kHZ clock for PWM control
tim = Timer(2, freq=1000)
motorA = tim.channel(1, Timer.PWM, pin=PWMA)
motorB = tim.channel(2, Timer.PWM, pin=PWMB)

def forward(value):
    A1.low()
    A2.high()
    B1.high()
    B2.low()
    motorA.pulse_width_percent(value)
    motorB.pulse_width_percent(value)

def back(value):
    A1.high()
    A2.low()
    B1.low()
    B2.high()
    motorA.pulse_width_percent(value)
    motorB.pulse_width_percent(value)

def stop():
    A1.low()
    A2.low()
    B1.low()
    B2.low()

forward(50)