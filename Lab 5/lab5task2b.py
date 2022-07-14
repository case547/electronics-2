import pyb
from pyb import Pin, Timer
from oled_938 import OLED_938

# Define pins to control motor directions and speed
A1 = Pin('X3', Pin.OUT_PP)
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1')
B1 = Pin('X7', Pin.OUT_PP)
B2 = Pin('X8', Pin.OUT_PP)
PWMB = Pin('X2')

# Configure timer 2 to produce 1kHZ clock for PWM control
tim = Timer(2, freq=1000)
motorA = tim.channel(1, Timer.PWM, pin=PWMA)
motorB = tim.channel(2, Timer.PWM, pin=PWMB)

pot = pyb.ADC(Pin('X11'))   # define potentiometer object as ADC conversion on X11

oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64,
                external_vcc=False, i2c_devid=60)   # Create 128x64 OLED display obj
oled.poweron()
oled.init_display()

# Define pins for motor speed sensors
A_sense = Pin('Y4', Pin.PULL_NONE)  # Pin.PULL_NONE = leave as input
B_sense = Pin('Y6', Pin.PULL_NONE)

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
A_state = 0         # prev state of A sensor
A_speed = 0         # latest motor A speed
A_count = 0         # positive transition count
B_state = 0
B_speed = 0
B_count = 0
tic = pyb.millis()  # keep time in ms

while True:
    # Detect rising edge on sensors
    if A_state == 0 and A_sense.value() == 1:
        A_count += 1
    A_state = A_sense.value()   # read val on A_sense pin   
    
    if B_state == 0 and B_sense.value() == 1:
        B_count += 1
    B_state = B_sense.value()

    # Check to see if 100 ms elapsed
    toc = pyb.millis()
    if toc - tic >= 100:
        A_speed = A_count
        B_speed = B_count
        
        # drive motor - controlled by potentiometer
        duty = round((pot.read()-2047.5)/20.475)
        
        oled.clear()
        oled.draw_text(0, 0, 'Pot5k value: {:5d}'.format(pot.read()))
        oled.draw_text(0, 15, 'Duty cycle: {:4d}'.format(duty))

        if duty >= deadzone:
            forward(duty)
        elif duty <= -deadzone:
            back(abs(duty))
        else:
            stop()

        A_count = 0
        B_count = 0
        
        # Display new speed
        oled.draw_text(0, 30, 'Motor A:{:5.2f} rps'.format(A_speed/39))
        oled.draw_text(0, 45, 'Motor B:{:5.2f} rps'.format(B_speed/39))	
        oled.display()
        tic = pyb.millis()