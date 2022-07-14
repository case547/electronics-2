import pyb
from pyb import Pin, Timer
from oled_938 import OLED_938

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP)  # control motor A direction
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1')            # control motor A speed

B1 = Pin('X7', Pin.OUT_PP)
B2 = Pin('X8', Pin.OUT_PP)
PWMB = Pin('X2')

pot = pyb.ADC(Pin('X11'))   # define potentiometer object as ADC conversion on X11

# Configure timer 2 to produce 1kHZ clock for PWM control
tim = Timer(2, freq=1000)
motorA = tim.channel(1, Timer.PWM, pin=PWMA)
motorB = tim.channel(2, Timer.PWM, pin=PWMB)

oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64,
                external_vcc=False, i2c_devid=60)   # Create 128x64 OLED display obj
oled.poweron()
oled.init_display()

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

deadzone = 5

while True:
    duty = round((pot.read()-2047.5)/40.95*2)

    oled.clear()
    oled.draw_text(0, 0, 'Pot5k value: {:5d}'.format(pot.read()))
    oled.draw_text(0, 20, 'Duty cycle: {:4d}%'.format(duty))

    if duty >= deadzone:
        forward(duty)
    elif duty <= -deadzone:
        back(abs(duty))
    else:
        stop()

    oled.display()