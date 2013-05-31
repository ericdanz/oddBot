import deviceclass, serial


def boot():
	#ping the components and find out what components are plugged in
	#and what their inputs/outputs are
	
	#for each port, send the boot command
	#get back the ios
	ser1 = serial.Serial('/dev/ttyAMA0', 9600)
	ser1.write('bx')
	s1string = ser1.readline()
	print s1string
	#if the port has an IO, put that into the correct component
	s1parse = s1string.split('/')
	component1 = deviceclass.component()
	component1.setport(1)
	component1.setcompnum(s1parse[1])
	for i in range(s1parse[3]):
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
	

	'''
	input1 = deviceclass.inout()
	input1.classOf = "Hand"
	input1.typeOf = "Boolean"
	input1.lowerBound = "0"
	input1.upperBound = "1"
	input1.granularity = "1.0"
	input1.state = "0"
	input1.isInput = "1"
	component1 = deviceclass.component()
	component1.addio(input1)
	component1.setcompnum(7)
	component1.setport(1)
	idevice = deviceclass.device()
	idevice.id = 10
	idevice.addcomp(component1)
	'''
	
	idevice = deviceclass.device()
	idevice.id = 10
	if(component1):
		idevice.addcomp(component1)
	if(component2):
		idevice.addcomp(component2)
	if(component3):
		idevice.addcomp(component3)
	return idevice
	
	

def getastate(port, i):
	#get a single IO's state
	#state format is now s/inputnumber
	sser = serial.Serial('/dev/ttyAMA0', 9600)
	sser.write('s/{}x'.format(i))
	stateresponse = sser.readline()
	#might have to parse state response to pull out the new state
	return stateresponse.split('/')[1]
	

def getstates(adevice):
	#ping the components and get the current state of their input/output
	sser = serial.Serial('/dev/ttyAMA0', 9600)
	sser.write('sx')
	stateresponse = sser.readline()
	#break it down by components, then by IOs
	for c in xrange(len(adevice.comps)):
		for i in xrange(len(adevice.comps[c].ios)):
			adevice.comps[c].ios[i].state = compconn.getastate(adevice.comps[c].port, i)
	
	return adevice
	
def doaction(port, action):
	#tell the proper component (known by its port) to have the proper input do the action
	
	aserial = serial.Serial('/dev/ttyAMA0',9600)
	aserial.write('i/{}/{}x'.format(action.actori,action.content))
	actionresponse = aserial.readline()
	
	return actionresponse