import pyb, time
from pyb import LED, ADC, Pin, Timer
from oled_938 import OLED_938
from mpu6050 import MPU6050

imu = MPU6050(1, False)

oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res':'Y8'}, height=64, external_vcc=False, i2c_devid=60)
oled.poweron()
oled.init_display()

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

# IMU connected to X9, X10
imu = MPU6050(1, False) # use I2C port 1 on PyBoard

motorA.pulse_width_percent(0)
motorB.pulse_width_percent(0)

trigger = pyb.Switch()
while not trigger():    # wait to tune K_p
    time.sleep(0.001)
    K_p = pot.read() * 15 / 4095 # use pot to set K_p
    oled.draw_text(0, 0, 'K_p = {:5.2f}'.format(K_p))
    oled.display()
while trigger(): pass   # wait for button release
while not trigger():    # wait to tune K_p
    time.sleep(0.001)
    K_i = pot.read() * 150 / 4095 # use pot to set K_i
    oled.draw_text(0, 10, 'K_i = {:5.2f}'.format(K_i))
    oled.display()
while trigger(): pass   # wait for button release
while not trigger():    # wait to tune K_d
    time.sleep(0.001)
    K_d = pot.read() * 1.5 / 4095 # use pot to set K_d
    oled.draw_text(0, 20, 'K_d = {:5.2f}'.format(K_d))
    oled.display()
while trigger(): pass   # wait for button release

print('Button pressed - Running')
oled.draw_text(0, 35, 'Running.')
oled.display()

def clamp(value, lower, upper):
    if value > upper:
        return upper
    elif value < lower:
        return lower
    return value

def pitch_estimate(pitch, dt, alpha):
    theta = imu.pitch()
    pitch_dot = imu.get_gy()
    pitch = alpha*(pitch + pitch_dot*dt) + (1-alpha)*theta
    return (pitch, pitch_dot)

last_error = None
i_term = 0   # summation of errors

def pid(pitch, setpoint, dt):
    global i_term
    global last_error

    # Compute proportional term
    error = setpoint - pitch
    p_term = K_p * error

    # Compute integral term
    i_term += K_i * error * dt  # accumulates
    i_term = clamp(i_term, min_output, max_output)

    # Compute derivative term
    try:
        d_error = error - last_error
    except:
        d_error = 0
    d_term = -K_d * d_error / dt

    # Compute final output
    output = p_term + i_term + d_term
    output = clamp(output, min_output, max_output)

    # Keep track of error state
    last_error = error

    return output

def drive(value):
    if value > 0:
        A1.high()
        A2.low()
        B1.low()
        B2.high()
        motorA.pulse_width_percent(abs(value))
        motorB.pulse_width_percent(abs(value))
    elif value < 0:
        A1.low()
        A2.high()
        B1.high()
        B2.low()
        motorA.pulse_width_percent(abs(value))
        motorB.pulse_width_percent(abs(value))
    else:
        A1.high()
        B1.high()
        A2.high()
        B2.high()
        motorA.pulse_width_percent(100)
        motorB.pulse_width_percent(100)

min_output = -100
max_output = 100

pitch = 0

tic = pyb.millis()
time.sleep(0.001)

while True:
    toc = pyb.millis()
    dt = (toc-tic)*0.001
    tic = pyb.millis()

    alpha = 0.9
    pitch, pitch_dot = pitch_estimate(pitch, dt, alpha)

    w = pid(pitch, 0, dt)
    drive(w)
    
    oled.draw_text(0, 35, 'Output: {:5.2f}'.format(w))
    oled.draw_text(0, 45, 'Pitch: {:5.2f}'.format(pitch))
    oled.display()