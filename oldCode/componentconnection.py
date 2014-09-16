import deviceclass, serial, time, threading
import multiprocessing

def readunreliable(instring, port):
	serialworked = 0
	#give it three chances, if there is no response then stop trying to talk to the port
	chances = 3
	print port
	port = '/dev/ttyO{}'.format(port)
	while not(serialworked):
		ser1 = serial.Serial(port, baudrate=9600, timeout=2)
		ser1.write(instring)
		respstring = ser1.readline()
		print respstring
		if not len(respstring):
			chances = chances - 1
			
		if not chances:
			return 'noresp'
		checkresponse = respstring.split('/')
		try:
			if checkresponse[1]:
				try:
					print "r index: {}".format(respstring.index('r'))
					print "check index: {}".format(respstring.index(instring[0]))
					serialworked = 1
				except ValueError:
					print "not the expected response:"
					print respstring
					time.sleep(.001)
					#respstring = ser1.readline()
					#print "clearing the serial buffer"
					#print respstring
					#respstring = ser1.readline()
					#print respstring
					#respstring = ser1.readline()
					#print respstring
					serialworked = 0
		except IndexError:
			serialworked = 0
		#time.sleep(.2)
	return respstring

def portboot(port, idevice):
	icomponent = deviceclass.component()
	icomponent.setport(port)
	icomponent.setclass("0")
	bootresponse = readunreliable('bx',port)
	if bootresponse!='noresp':
			print 'Rebuilding my internal model for port {}'.format(port[x])
			#if the port has an IO, put that into the correct component
			parsestring = bootresponse.split('/')
			print parsestring[1]
			icomponent.setcompnum(int(parsestring[1]))
			print parsestring[4].split(',')[0]
			icomponent.setclass(parsestring[4].split(',')[0])
			
			print parsestring[3]
			for i in range(int(parsestring[3])):
				print "Configuring IOs"
				io = deviceclass.inout()
				io.classOf = parsestring[4].split(',')[i]
				io.typeOf = parsestring[5].split(',')[i]
				io.isInput = parsestring[6].split(',')[i]
				io.lowerBound = parsestring[7].split(',')[i]
				io.upperBound = parsestring[8].split(',')[i]
				io.granularity = parsestring[9].split(',')[i]
				io.state = 0
				icomponent.addio(io)
	else:
		icomponent.setcompnum(0)
	print icomponent.compid
	idevice.addcomp(icomponent)
	
def boot(checkdevice):
	#ping the components and find out what components are plugged in
	#and what their inputs/outputs are
	
	#set up the device
	idevice = deviceclass.device()
	idevice.id = 10
	#for each port, send the boot command
	#get back the ios
	print "Checking what is connected"
	#serial ports
	"""
	port = ['1', '2', '4']
	for x in xrange(len(port)):
		#check each port with a boot command
		bootresponse = readunreliable('bx',port[x])
		#each port gets a blank component
		icomponent = deviceclass.component()
		icomponent.setport(port[x])
		icomponent.setclass("0")
		
		if bootresponse!='noresp':
			print 'Rebuilding my internal model for port {}'.format(port[x])
			#if the port has an IO, put that into the correct component
			parsestring = bootresponse.split('/')
			print parsestring[1]
			icomponent.setcompnum(int(parsestring[1]))
			print parsestring[4].split(',')[0]
			icomponent.setclass(parsestring[4].split(',')[0])
			
			print parsestring[3]
			for i in range(int(parsestring[3])):
				print "Configuring IOs"
				io = deviceclass.inout()
				io.classOf = parsestring[4].split(',')[i]
				io.typeOf = parsestring[5].split(',')[i]
				io.isInput = parsestring[6].split(',')[i]
				io.lowerBound = parsestring[7].split(',')[i]
				io.upperBound = parsestring[8].split(',')[i]
				io.granularity = parsestring[9].split(',')[i]
				io.state = 0
				icomponent.addio(io)
		else:
			icomponent.setcompnum(0)
		print icomponent.compid
		idevice.addcomp(icomponent)
	"""
	#USE POOL
	port = ['1', '2', '4']
	pool = multiprocessing.Pool(processes=int(len(port)))
	result = []
	for x in xrange(len(port)):
		#call process portboot for port[x]
		result.append(pool.apply_async(portboot, (port[x], idevice)))
		#t = threading.Thread(target=portboot, args=(port[x], idevice))
		#t.start()
	
	#could add the components via result[x].get() if passing through doesn't work
	time.sleep(1)
	
	#Check that the devices are the same. If checkdevice is 0 this is the initial boot
	if not (checkdevice == 0):
		for c in xrange(len(idevice.comps)):
			for i in xrange(len(idevice.comps[c].ios)):
				#if the devices have the same components with the same inputs
				try:
					if (idevice.comps[c].ios[i].isInput == checkdevice.comps[c].ios[i].isInput) and (idevice.comps[c].ios[i].lowerBound == checkdevice.comps[c].ios[i].lowerBound) and (idevice.comps[c].ios[i].upperBound == checkdevice.comps[c].ios[i].upperBound) and (idevice.comps[c].ios[i].granularity == checkdevice.comps[c].ios[i].granularity) and (idevice.comps[c].ios[i].classOf == checkdevice.comps[c].ios[i].classOf) and (idevice.comps[c].ios[i].typeOf == checkdevice.comps[c].ios[i].typeOf) and (idevice.comps[c].compid == checkdevice.comps[c].compid) and (idevice.comps[c].port == checkdevice.comps[c].port):
						print 'the boot was cancelled: both devices are the same'
						return 'same'
				except IndexError:
					print 'null now something, continue boot'
				
	'''
	s1string = readunreliable('bx', '/dev/ttyO4')
	#print s1string
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
				'''
		#ser2 = serial.Serial('/dev/tty/port2', 9600)
	

	
		
		#if(component1):
		#	idevice.addcomp(component1)
		#if(component2):
		#	idevice.addcomp(component2)
		#if(component3):
		#	idevice.addcomp(component3)
		
		
	return idevice

	
	

def getastate(port, i, io):
	#get a single IO's state
	#state format is now s/inputnumber
	#sser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
	#sser.write('s/{}x'.format(i))
	while (1):
		print 'from io {}'.format(i)
		stateresponse = readunreliable('s/{}x'.format(i), port)
		print stateresponse
		res2 = stateresponse.split('rs')[1]
		
		print res2.split('/')[1]
		#might have to parse state response to pull out the new state
		#return res2.split('/')[1]
		
		#put the state right into the component - through a function 
		#that doesn't pass through automatically
		#putstate(port, i, res2.split('/')[1])
		
		#pass it through directly
		io.state = res2.split('/')[1]
		time.sleep(1)

		

def getstates(adevice):
	#ping the components and get the current state of their input/output
	
	#break it down by components, then by IOs
	'''
	xio = 0
	for c in xrange(len(adevice.comps)):
		for i in xrange(len(adevice.comps[c].ios)):
			adevice.comps[c].ios[i].state = getastate(adevice.comps[c].port, i)
	'''
	#multiproc style - learn how to kill processes
	xio = 0
	for c in xrange(len(adevice.comps)):
		for i in xrange(len(adevice.comps[c].ios)):
			p = multiprocessing.Process(target=getastate,args=(adevice.comps[c].port,i))
			p.start()
	return 1
	
def doaction(rawdata):
	#tell the proper component (known by its port) to have the proper input do the action
	
	actionresponse = readunreliable('i/{}/{}x'.format(rawdata[3],rawdata[4]), rawdata[1])
	
	return actionresponse
