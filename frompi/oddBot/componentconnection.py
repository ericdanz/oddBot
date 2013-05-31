import deviceclass, serial, time


def readunreliable(instring, port):
	serialworked = 0
	while (serialworked):
		ser1 = serial.Serial(port, baudrate=9600, timeout=1)
		ser1.write(inputstring)
		respstring = ser1.readline()
		checkresponse = respstring.split('/')
		if checkresponse[1]:
			serialworked = 1
		time.sleep(1)
	return respstring

def boot():
	#ping the components and find out what components are plugged in
	#and what their inputs/outputs are
	'/dev/ttyAMA0'
	#for each port, send the boot command
	#get back the ios
	print "Checking what is connected"
	s1string = readunreliable('bx', '/dev/ttyAMA0')
	print s1string
	if(s1string):
		print "Rebuilding my internal model"
		#if the port has an IO, put that into the correct component
		s1parse = s1string.split('/')
		component1 = deviceclass.component()
		component1.setport(1)
		print s1parse[1]
		component1.setcompnum(int(s1parse[1]))
		print s1parse[3]
		for i in range(int(s1parse[3])):
			io = deviceclass.inout()
			io.classOf = s1parse[4].split(',')[i]
			io.typeOf = s1parse[5].split(',')[i]
			io.isInput = s1parse[6].split(',')[i]
			io.lowerBound = s1parse[7].split(',')[i]
			io.upperBound = s1parse[8].split(',')[i]
			io.granularity = s1parse[9].split(',')[i]
			io.state = s1parse[7].split(',')[i]
			component1.addio(io)
				
		#ser2 = serial.Serial('/dev/tty/port2', 9600)
	

	
		idevice = deviceclass.device()
		idevice.id = 10
		if(component1):
			idevice.addcomp(component1)
		#if(component2):
		#	idevice.addcomp(component2)
		#if(component3):
		#	idevice.addcomp(component3)
		return idevice

	return 0
	
	

def getastate(port, i):
	#get a single IO's state
	#state format is now s/inputnumber
	#sser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
	#sser.write('s/{}x'.format(i))
	stateresponse = readunreliable('s/{}x'.format(i), '/dev/ttyAMA0')
	print stateresponse
	res2 = stateresponse.split('rs')[1]
	
	print res2.split('/')[1]
	#might have to parse state response to pull out the new state
	return res2.split('/')[1]
	

def getstates(adevice):
	#ping the components and get the current state of their input/output
	
	#break it down by components, then by IOs
	xio = 0
	for c in xrange(len(adevice.comps)):
		for i in xrange(len(adevice.comps[c].ios)):
			adevice.comps[c].ios[i].state = getastate(adevice.comps[c].port, i)
	
	return adevice
	
def doaction(port, action):
	#tell the proper component (known by its port) to have the proper input do the action
	
	#aserial = serial.Serial('/dev/ttyAMA0',9600)
	#aserial.write('i/{}/{}x'.format(action.actori,action.content))
	actionresponse = readunreliable('i/{}/{}x'.format(action.actori,action.content), '/dev/ttyAMA0')
	
	return actionresponse
