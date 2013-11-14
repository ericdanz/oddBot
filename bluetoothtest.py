import bluetooth

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
	print "Name: "
	print bluetooth.lookup_name(bdaddr)
	print "Address: "
	print bdaddr