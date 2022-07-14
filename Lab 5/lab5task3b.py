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

# Initisalise variables
deadzone = 5
duty = 0
A_speed = 0         # latest motor A speed
A_count = 0         # positive transition count
B_speed = 0
B_count = 0

#----- Section to set up interrupts -----
def isr_motorA(dummy):  # motor sensor ISR - just count transitions
    global A_count
    A_count += 1    # incremented every time interrupt occurs on Y4 sensor signal

def isr_motorB(dummy):
    global B_count
    B_count += 1

def isr_speed_timer(dummy): # timer interrupt at 100ms intervals - called when Timer 4 period over
    global A_count
    global A_speed
    global B_count
    global B_speed
    A_speed = A_count   # remember count val
    B_speed = B_count
    A_count = 0         # reset count
    B_count = 0

# Create external interrupts for Hall effect sensors
import micropython
micropython.alloc_emergency_exception_buf(100)
from pyb import ExtInt

motorA_int = ExtInt('Y4', ExtInt.IRQ_RISING, Pin.PULL_NONE, isr_motorA)
motorB_int = ExtInt('Y6', ExtInt.IRQ_RISING, Pin.PULL_NONE, isr_motorB)

# Create timer intterupts at 100ms intervals
speed_timer = pyb.Timer(4, freq=10)
speed_timer.callback(isr_speed_timer)

#----- End of interrupt section -----

while True: # no polling func: sensor signal on Y4 not used nor is elapsed time checked
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
    
    # Display new speed
    oled.draw_text(0, 30, 'Motor A:{:5.2f} rps'.format(A_speed/39))
    oled.draw_text(0, 45, 'Motor B:{:5.2f} rps'.format(B_speed/39))	
    oled.display()