import bluetooth
import deviceclass

#sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#find a bluetooth device on the correct service
def findservice(muuid, sock):
	service_matches = bluetooth.find_service(uuid = muuid)
	if len(service_matches) == 0:
		print "No matches for insecure"
		return 0
	else:
		for match in service_matches:
			print match
			print "{name} {host} {port}".format(**match)
			mhost = match['host']
			mport = match['port']

	sock.connect((mhost,mport))
	return 1


#push device information
def pushconfig(adevice, sock):
	hasLocomotion = 0;
	hasInteraction = 0;
	hasCamera = 0;
	
	for c in adevice.comps:
		if c.classOf == 'Locomotion':
			hasLocomotion = 1;
		elif c.classOf == 'Interaction':
			hasInteraction = 1;
		elif c.classOf == 'Camera':
			hasCamera = 1;
	
	outString = "CONF L{} I{} C{}".format(hasLocomotion,hasInteraction,hasCamera)
	try:
		sock.send(outString)
	except e:
		return 0
	
	return 1
	
			
		
		
	
#generic send
def send(sock, data):
	try:
		sock.send(data)
	except e:
		return 0
	
	return 1
	
#generic listen
def listen(sock):
	data = 0
	while(1):
		data = sock.recv(1024)
		if data:
			return data
			

		
#push states
def pushstates(adevice, sock):
	#push all states
	#declare a null restring in case there are no ios in components
	restring = "no ios"
	for c in xrange(len(adevice.comps)):
		for i in xrange(len(adevice.comps[c].ios)):
			datastring = "{}/{}/{}".format(i,adevice.comps[c].ios[i].state,adevice.comps[c].compid)
			#check if it is an image and send the image not the reference
			#NOT YET ACTIVE
			restring = send(sock, datastring)
			if not restring:
				return restring
	return restring

	
	
