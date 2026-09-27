#Pins:
#Raspberry Pi Pin NFC RFID Module
#Pin 6 = GND
#Pin 2= VCC
#Pin 3 =SDA
#Pin 5 =SCL

#Enter the following Commands:
#sudo raspi-config (enable i2c)
#[interface -> enable i2c->finish)
#pip3 install adafruit-circuitpython-pn532 --break-system-packages
#Enter the following Python Programs:in thorny

#Program 1: to verify the card number

import board
import busio
from adafruit_pn532.i2c import PN532_I2C
i2c = busio.I2C(board.SCL, board.SDA)
pn532= PN532_I2C(i2c)
ic, ver, rev, support = pn532.firmware_version print(f"successs! Found PN532 with Fireware: {ver}.{rev}")
print("Place your blue fob or white card on the red board...")
while True:
uid= pn532.read_passive_target(timeout=0.5)
if uid is not None:
print(f"Found Tag! ID is : {[hex(i) for i in uid]}")

#Program 2: Write the data
import board
import busio
from adafruit_pn532.i2c import PN532_I2C
# Setup I2C
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c)
print("--- NFC Writer ---")
text_to_write = input("Enter a small message to save to the card: ")
# Data must be exactly 16 bytes for a single block
# We pad the text with spaces if it's too short
data = text_to_write.ljust(16).encode()
print("Now, place your white card on the reader...")
while True:
uid = pn532.read_passive_target(timeout=0.5)
if uid is not None:
try:
# We use block 4 (Sector 1) to avoid messing with system blocks # This requires a 'default' key for Mifare cards
key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
if pn532.mifare_classic_authenticate_block(uid, 4, 0x60, key):
pn532.mifare_classic_write_block(4, data)
print(f"Success! '{text_to_write}' written to card.")
break
else:
print("Authentication failed!")
except Exception as e:
print(f"Error: {e}")
break

#Program 3: Read the data

import board
import busio
from adafruit_pn532.i2c import PN532_I2C
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c)
print("Waiting for card to read stored data...")
while True:
uid = pn532.read_passive_target(timeout=0.5)
if uid is not None: key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
if pn532.mifare_classic_authenticate_block(uid, 4, 0x60, key):
data = pn532.mifare_classic_read_block(4)
if data is not None:
print(f"Stored Data: {data.decode().strip()}")
break

#Q2. Write a program to display unique ID for the input data using RFID module.

#Command:
#Command 1: sudo raspi-config (enable i2c)
#Command 2: sudo reboot
#Command 3: pip3 install adafruit-circuitpython-pn532 --break-system-packages
#Command 3: sudo apt install -y libnfc-bin libnfc-dev libusb-dev libpcsclite-dev i2c-tools
#Command 4: sudo nano /etc/nfc/libnfc.conf
#device.name = "PN532 over I2C"
#device.connstring = "pn532_i2c:/dev/i2c-1"
#Save the file.

#Command 5:
 #i2cdetect –y 1 (optional put sudo)
#Command 6:
 #nfc-list
#Enter the following Python program in thonny.

import subprocess
import time
NAME = "Upasana" # Put your name here
last_uid = None
try:
 while True:
 output = subprocess.getoutput("nfc-list")
 if "UID" in output:
 for line in output.splitlines():
 if "UID" in line:
 uid = line.split(":")[1].strip().replace(" ", "")
 if uid != last_uid:
 print(f"{NAME}: {uid}")
 last_uid = uid
 break time.sleep(1)
except KeyboardInterrupt:
 print("\nStopped")

