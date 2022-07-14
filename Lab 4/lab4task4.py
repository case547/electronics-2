'''Lab 4 Task 4'''

import pyb                      # Pyboard basic library
from pyb import LED, ADC, Pin   # Various class libraries in pyb
from oled_938 import OLED_938   # OLED display driver

# Create peripheral objects
b_LED = LED(4)          # Blue LED
pot = ADC(Pin('X11'))   # 5k-ohm potentiometer to ADC input on pin X11

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64,
                external_vcc=False, i2c_devid=60)   # Create 128x64 OLED display obj
oled.poweron()
oled.init_display()

tic = pyb.millis()          # Store start time
while True:
    b_LED.toggle()
    toc = pyb.millis()      # Read elapsed time

    oled.clear()
    # Simple hello message
    oled.draw_text(22,0,'Hello there.')  # Each char is 6x8 pixels
    oled.draw_text(0,20,'Delay time:{:6.3f}sec'.format((toc-tic)*0.001))
    oled.draw_text(0,40,'POT5k reading:')
    oled.draw_text(50,50,'{:5d}'.format(pot.read()))# Measure potentiometer voltage

    angle = -round((pot.read() - 2047.5)/22.75)
    oled.line(23, 40, angle, 15, 1)

    tic = pyb.millis()      # Start time
    oled.display()
    delay = pyb.rng()%1000  # Generate random number between 0 and 999
    pyb.delay(delay)