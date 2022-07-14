'''Challenge 2'''

import pyb
from pyb import LED, Pin, Timer
from oled_938 import OLED_938
from mpu6050 import MPU6050

# Define LED
b_LED = LED(4)

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

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64,
                external_vcc=False, i2c_devid=60)   # Create 128x64 OLED display obj
oled.poweron()
oled.init_display()
oled.draw_text(0, 0, "Challenge 2")
oled.display()

# IMU connected to X9, X10
imu = MPU6050(1, False) # use I2C port 1 on PyBoard

# Define pins for motor speed sensors
A_sense = Pin('Y4', Pin.PULL_NONE)  # Pin.PULL_NONE = leave as input
B_sense = Pin('Y6', Pin.PULL_NONE)

def read_imu(dt, alpha):
    global pitch
    global roll

    theta = imu.pitch()
    phi = imu.roll()

    pitch = alpha*(pitch + imu.get_gy()*dt*0.001) + (1-alpha)*theta
    roll = alpha*(roll + imu.get_gx()*dt*0.001) + (1-alpha)*phi

    oled.draw_text(0, 15, "Pitch: {:3d}".format(round(pitch)))
    oled.draw_text(0, 25, "Roll: {:3d}".format(round(roll)))

    oled.display()

def A_forward(value):
    A1.low()
    A2.high()
    motorA.pulse_width_percent(value)

def A_back(value):
    A1.high()
    A2.low()
    motorA.pulse_width_percent(value)

def A_stop():
    A1.low()
    A2.low()    

def B_forward(value):
    B1.high()
    B2.low()
    motorB.pulse_width_percent(value)

def B_back(value):
    B1.low()
    B2.high()
    motorB.pulse_width_percent(value)

def B_stop():
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

# Create external interrupts for motor A's Hall effect sensor
import micropython
micropython.alloc_emergency_exception_buf(100)
from pyb import ExtInt

motorA_int = ExtInt('Y4', ExtInt.IRQ_RISING, Pin.PULL_NONE, isr_motorA)
motorB_int = ExtInt('Y6', ExtInt.IRQ_RISING, Pin.PULL_NONE, isr_motorB)

# Create timer intterupts at 100ms intervals
speed_timer = pyb.Timer(4, freq=10)
speed_timer.callback(isr_speed_timer)

#----- End of interrupt section -----

pitch = 0
roll = 0
tic = pyb.millis()
while True:
    b_LED.toggle()
    toc = pyb.millis()
    read_imu(toc-tic, 0.7)
    
    A_duty = round(pitch/0.9)
    B_duty = round(roll/0.9)

    if A_duty >= deadzone:
        A_forward(A_duty)
    elif A_duty <= -deadzone:
        A_back(abs(A_duty))
    else:
        A_stop()

    if B_duty >= deadzone:
        B_forward(B_duty)
    elif B_duty <= -deadzone:
        B_back(abs(B_duty))
    else:
        B_stop()

    # Display new speed
    oled.draw_text(0, 40, 'Motor A:{:5.2f} rps'.format(A_speed/39))
    oled.draw_text(0, 50, 'Motor B:{:5.2f} rps'.format(B_speed/39))	
    oled.display()

    tic = pyb.millis()