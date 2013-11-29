import urllib2, httplib
import bluetooth
import componentconnection as compconn
import blueconnection as blueconn
import deviceclass
import time 

muuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
blueconn.findservice(muuid,sock)
hresponse = ""
#wait until sock is connected
notconnected = 1
while(notconnected):
	try:
		sock.getpeername(self)
		print sock.getpeername(self)
		notconnected = 0
	except IOError:
		notconnected = 1
		


#time.sleep(2)

mydevice = deviceclass.device()   
mydevice.id = 10
print "Starting"
		   
#boot
mydevice = compconn.boot(0)
#mydevice.addcomp(fakecomp)

print "Booted"
time.sleep(3)
#push config to server
hresponse = blueconn.pushconfig(mydevice, sock)
if hresponse:
	print "Config Sent"
else:
	print "Error sending config"

print "Get States from Components"
#get states of components
hresponse = compconn.getstates(mydevice)
if hresponse:
	print "Get-state processes started"
else:
	print "Error with getstates"

print "Push States"
#push those states to server
#use a new process
p = multiprocessing.Process(target=blueconn.pushstates,args=(mydevice, sock))
p.start()
		

#LOOP THIS PART
boo = 1
counter = 0
print "starting loop"

while(boo):
	#if at any point there is an error
	#set boo = 0
	
	#this is a hack to aid debugging
	counter +=1
	if (counter > 65):
		boo = 0
	
	#if its a tenth loop, check devices by booting
	if not (counter%20):
		print "Checking if same components are connected"
		checkdevice = compconn.boot(mydevice)
		if not (checkdevice == 'same'):
			mydevice = checkdevice
			hresponse = blueconn.pushconfig(mydevice, sock)
			print "Config Response: ", hresponse
			
		
	print "Get Actions from Server"
	#get action from server		   
	rawdata = blueconn.listen(sock)
	if (rawdata):
		print "Raw Data: {}".format(rawdata)
		rawdata.replace(" ","")
		rawdata = rawdata.split('/')
		print "Do Actions"
		#do the action
		#get the component from the action.actorc
		aresponse = compconn.doaction(rawdata)
		print aresponse.split('/')[2]
		
		'''
		#this is a hack that works around having no actual components
		for i in xrange(len(mydevice.comps)):
			if (mydevice.comps[i].compid == action.actorc):
				compNum = i
		mydevice.comps[comp_id].ios[action.actori] = compconn.doaction(mydevice.comps[comp_id].ios[action.actori],action)
		'''
	
	else:
		print "No Actions"
	
	
	
	
	#no longer needed because of multiprocess
	
	#print "Get States from Components"
	#get states of components
	#mydevice = compconn.getstates(mydevice)

	print "Push States"
	#(do this even if the rest above failed)
	#push those states to server
	hresponse = blueconn.pushstates(mydevice, sock)
	print "States response: {}".format(hresponse)
	time.sleep(.1)
	


#END LOOP
print "End of Program"




