import bluetooth, time
import blueconnection as blueconn


muuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
blueconn.findservice(muuid,sock)
notconnected = 1
while(notconnected):
	try:
		if sock.getpeername()[1] == 0:
			notconnected = 1
			time.sleep(.5)
		else:
			notconnected = 0
	except IOError:
		notconnected = 1
boo = 1
while (boo):
	rawdata = blueconn.listen(sock)
	if (rawdata):
		print "Raw Data: {}".format(rawdata)
	if (rawdata == 'end')
		boo = 0

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
	print "Name: "
	print bluetooth.lookup_name(bdaddr)
	print "Address: "
	print bdaddr
