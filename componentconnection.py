import deviceclass, serial


def boot():
	#ping the components and find out what components are plugged in
	#and what their inputs/outputs are
	
	#for each port, send the boot command
	#get back the ios
	ser1 = serial.Serial('/dev/tty/port1', 9600)
	ser1.write('b/1')
	ser1.readline()
	#if the port has an IO, put that into the correct component

	ser2 = serial.Serial('/dev/tty/port2', 9600)
	


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
	return idevice

def getastate(io):
	#get a single IO's state
	return io.state

def getstates(adevice):
	#ping the components and get the current state of their input/output
	
	#break it down by components
	
	#break it down by the IOs
	
	
	return adevice
	
def doaction(acomponent, action):
	#tell the proper component (known by its port) to have the proper input do the action
	
	aserial = serial.Serial('/dev/tty/port{}'.format(acomponent.port),9600)
	aserial.write('i/{}/{}'.format(action.actori,action.content))
	actionresponse = aserial.readline()
	
	return actionresponse