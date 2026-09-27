#GND = 14pin
#VCC=4pin
#DIO= 18pin
#CLK= 16pin


#Execute the following Commands: 
#pip install RPi.GPIO --break-system-packages
#Download 7segment code  from link: 
#https://github.com/bhoomikapansare/7Segment.git
#copy the code from tml1637.py
#and paste in Thronny and run


import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

SEGMENTS = [
    0x3F,  # 0
    0x06,  # 1
    0x5B,  # 2
    0x4F,  # 3
    0x66,  # 4
    0x6D,  # 5
    0x7D,  # 6
    0x07,  # 7
    0x7F,  # 8
    0x6F   # 9
]

class TM1637:
    def __init__(self, clk=23, dio=24, brightness=1):
        self.clk = clk
        self.dio = dio
        self.brightness = brightness
        self.doublepoint = False

        if not GPIO.getmode():
            GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.clk, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.dio, GPIO.OUT, initial=GPIO.HIGH)

        self._start()
        self._write_byte(0x40)
        self._stop()
        self.SetBrightness(brightness)
        self.Clear()

    def _start(self):
        GPIO.output(self.dio, GPIO.HIGH)
        GPIO.output(self.clk, GPIO.HIGH)
        GPIO.output(self.dio, GPIO.LOW)

    def _stop(self):
        GPIO.output(self.clk, GPIO.LOW)
        GPIO.output(self.dio, GPIO.LOW)
        GPIO.output(self.clk, GPIO.HIGH)
        GPIO.output(self.dio, GPIO.HIGH)

    def _write_byte(self, data):
        for i in range(8):
            GPIO.output(self.clk, GPIO.LOW)
            GPIO.output(self.dio, data & 0x01)
            data >>= 1
            GPIO.output(self.clk, GPIO.HIGH)

        GPIO.output(self.clk, GPIO.LOW)
        GPIO.setup(self.dio, GPIO.IN)
        GPIO.output(self.clk, GPIO.HIGH)
        GPIO.setup(self.dio, GPIO.OUT)

    def SetBrightness(self, brightness):
        brightness = max(0, min(7, brightness))
        self.brightness = brightness
        self._start()
        self._write_byte(0x88 + brightness)
        self._stop()

    def ShowDoublepoint(self, on):
        self.doublepoint = on

    def Show(self, data):
        self._start()
        self._write_byte(0x40)
        self._stop()

        self._start()
        self._write_byte(0xC0)

        for i in range(4):
            seg = SEGMENTS[data[i]]
            if i == 1 and self.doublepoint:
                seg |= 0x80
            self._write_byte(seg)

        self._stop()

    def Clear(self):
        self.Show([0, 0, 0, 0])
