import pyb, time
from pyb import LED, ADC, Pin, Timer
from oled_938 import OLED_938
from mpu6050 import MPU6050
from motor import DRIVE

m = DRIVE()
# IMU connected to X9, X10
imu = MPU6050(1, False) # use I2C port 1 on PyBoard

oled = OLED_938(pinout={'sda':'Y10', 'scl':'Y9', 'res':'Y8'}, height=64, external_vcc=False, i2c_devid=60)
oled.poweron()
oled.init_display()
oled.draw_text(0, 0, 'Running Challenge 3')
oled.display()

def clamp(value, lower, upper):
    '''Constrains value to [lower, upper]'''
    if value > upper:
        return upper
    elif value < lower:
        return lower
    return value

def pitch_estimate(pitch, dt, alpha):
    '''Estimates p[n] given p[n-1], and a[n] and g[n] readings''' 
    theta = imu.pitch()
    pitch_dot = imu.get_gy()
    pitch = alpha*(pitch + pitch_dot*dt) + (1-alpha)*theta
    return (pitch, pitch_dot)

last_A = None
last_B = None

def pid(setpoint, cpe_A, cpe_B, dt):
    '''The PID controller'''
    global last_A
    global last_B

    # Compute proprtional terms
    aError = setpoint - m.get_speedA()
    bError = setpoint - m.get_speedB()
    p_A = K_p * aError
    p_B = K_p * bError

    # Compute cumulative error terms, and prevent integral windup
    cpe_A += aError * dt
    cpe_B += bError * dt
    i_A = clamp(K_i * cpe_A, min_output, max_output)
    i_B = clamp(K_i * cpe_B, min_output, max_output)

    # Compute difference terms
    try:
        diff_A = aError - last_A
        diff_B = bError - last_B
    except:
        diff_A = diff_B = 0

    d_A = K_d * diff_A / dt
    d_B = K_d * diff_B / dt

    # Compute final output, and constrain to +/- 100
    output_A = p_A + i_A - d_A
    output_B = p_B + i_B - d_B
    output_A = clamp(output_A, min_output, max_output)
    output_B = clamp(output_B, min_output, max_output)

    # Keep track of error state
    last_A = aError
    last_B = bError

    return (output_A, output_B, cpe_A, cpe_B)

def changeSpeed(duty_A, duty_B, output_A, output_B):
    '''Adjusts motor speed base on current duty cycle and PID output'''
    duty_A += output_A
    duty_B += output_B
    duty_A = clamp(duty_A, -100, 100)
    duty_B = clamp(duty_B, -100, 100)

    print(round(duty_A), round(duty_B))
    
    m.right_forward(duty_A)
    m.left_forward(duty_B)

    return (duty_A, duty_B)

K_p = 1
K_i = 0.5
K_d = 0.2

min_output = -100
max_output = 100

cpe_A = cpe_B = 0

duty_A = duty_B = 0
setpoint = 0

pitch = 0
alpha = 0.9

tic = pyb.millis()
time.sleep(0.001)

while True:
    toc = pyb.millis()
    dt = (toc-tic)/1000
    tic = pyb.millis()
    A, B, cpe_A, cpe_B = pid(setpoint, cpe_A, cpe_B, dt)

    duty_A, duty_B = changeSpeed(duty_A, duty_B, A, B)

    pitch, pitch_dot = pitch_estimate(pitch, dt, alpha)
    setpoint = abs(pitch)/3

    oled.draw_text(0, 15, 'Pitch: {:5.2f}'.format(pitch))
    oled.draw_text(0, 25, 'Set point: {:5.2f}'.format(setpoint))
    oled.draw_text(0, 40, 'speedA = {:5.2f} rps'.format(m.get_speedA()))
    oled.draw_text(0, 50, 'speedB = {:5.2f} rps'.format(m.get_speedB()))
    oled.display()
