#sudo raspi-config (enable i2c) 
#pip install board --break-system-packages 
#sudo pip install drawnow --break-system-packages 
#sudo apt-get install -y i2c-tools python3-smbus 
#python3 -m pip install --upgrade --no-cache-dir adafruit-blinka adafruit-circuitpython-busdevice adafruit-circuitpython-ads1x15 --break-system-packages


#VDD = Pin 1
#GND = Pin 6
#SDA =pin3
#SCL =pin5


from collections import deque
import time
import board
import busio
import numpy as np
import matplotlib.pyplot as plt

from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
from matplotlib.animation import FuncAnimation

# ================= SETTINGS =================
DURATION = 10          # seconds shown on screen
SAMPLE_RATE = 128      # ADS1115: 8–860 SPS
GAIN = 1              # ±4.096V
CHANNEL = 0           # A0
I2C_ADDRESS = 0x48
# ============================================

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# ADC setup
ads = ADS1115(i2c, address=I2C_ADDRESS)
ads.data_rate = SAMPLE_RATE
ads.gain = GAIN

chan = AnalogIn(ads, CHANNEL)

# Buffer
num_samples = SAMPLE_RATE * DURATION
x = np.linspace(0, DURATION, num_samples)
y = deque([0.0] * num_samples, maxlen=num_samples)

# Plot
fig, ax = plt.subplots()
ax.set_xlim(0, DURATION)
ax.set_ylim(-4.2, 4.2)
ax.set_xlabel("Time [s]")
ax.set_ylabel("Voltage [V]")
ax.set_title("ADS1115 Software Oscilloscope")
ax.grid(True)

line, = ax.plot(x, y, lw=1)

# Update loop
def update(frame):
    try:
        voltage = chan.voltage
    except Exception:
        voltage = 0.0

    y.append(voltage)
    line.set_ydata(y)
    return line,

# Animation
ani = FuncAnimation(
    fig,
    update,
    interval=1000 / SAMPLE_RATE,
    blit=True
)

plt.show()


#save and run
