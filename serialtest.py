import serial
from serial import SEVENBITS, STOPBITS_ONE, PARITY_EVEN, EIGHTBITS, PARITY_NONE
import time

serialport = serial.Serial(port="/dev/ttyO4", baudrate=9600, bytesize=8, timeout=1)
rply = serialport.read(400)
serialport.write("bx")
time.sleep(4)
reply = serialport.read(90)
print reply

serialport.write("bx")
reply = serialport.read(90)
print reply
time.sleep(3)
serialport.write("s/0x")


time.sleep(2)

while(1):
	serialport.write("i/0/1x")
	time.sleep(1)
	serialport.write("i/0/0x")
	time.sleep(2)
	reply = serialport.read(90)
	print reply
