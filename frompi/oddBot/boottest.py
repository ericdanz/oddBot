import componentconnection as compconn
import deviceclass
import serial, time

#mydevice = deviceclass.device()
#mydevice.id = 10
print "Starting"

ser1 = serial.Serial(port = '/dev/ttyAMA0', baudrate=9600)
#reply = ser1.read(90)
print "Sending"

ser1.write('bx')
reply = ser1.readline()
print "Booting: "
print reply

mydevice = compconn.boot()

print "Boot Complete"
