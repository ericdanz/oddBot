import sys
import bluetooth

muuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"
service_matches = bluetooth.find_service(uuid = muuid)

if len(service_matches) == 0:
	print "No matches for insecure"
	sys.exit(0)
else:
	for match in service_matches:
		print match
		print "{name} {host} {port}".format(**match)
		mhost = match['host']
		mport = match['port']

		
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((mhost,mport))
sock.send("hello!")
while(1):
	mbuffer = sock.recv(1024)
	print mbuffer
	if mbuffer == 'exit':
		sys.exit(0)
sock.close()
