import urllib2, httplib
import componentconnection as compconn
import serverconnection as servconn
import deviceclass

hresponse = ""

mydevice = deviceclass.device()   
mydevice.id = 10
		   
#boot
mydevice = compconn.boot()
#push config to server
hresponse = servconn.pushconfig(mydevice)
print "Config Response: ", hresponse

print "Get States from Components"
#get states of components
for c in xrange(len(mydevice.comps)):
	for i in xrange(len(mydevice.comps[c].ios)):
		mydevice.comps[c].ios[i].state = compconn.getstates(mydevice.comps[c].ios[i])

print "Push States"
#push those states to server
for c in xrange(len(mydevice.comps)):
	for i in xrange(len(mydevice.comps[c].ios)):
		hresponse = servconn.pushstates(i,mydevice.comps[c].ios[i].state,mydevice.comps[c].compid)
		


#LOOP THIS PART
e = 1
counter = 0
print "starting loop"

while(e):
	#if at any point there is an error
	#set e = 0
	
	#this is a hack to aid debugging
	counter +=1
	if (counter > 3):
		e = 0
	
	print "Get Actions from Server"
	#get action from server		   
	action = servconn.getaction(mydevice.id)
	if (action):
		print "Action: ",action.content
	
	
		#confirm you recieved action
		hresponse = servconn.confaction(action)
			
		print "Do Actions"
		#do the action
		#get the component from the action.actorc
		for i in xrange(len(mydevice.comps)):
			if (mydevice.comps[i].compid == action.actorc):
				compNum = i
		aresponse = compconn.doaction(mydevice.comps[compNum], action)
		'''
		#this is a hack that works around having no actual components
		for i in xrange(len(mydevice.comps)):
			if (mydevice.comps[i].compid == action.actorc):
				compNum = i
		mydevice.comps[comp_id].ios[action.actori] = compconn.doaction(mydevice.comps[comp_id].ios[action.actori],action)
		'''
	else:
		print "no actions"
	
	print "Get States from Components"
	#get states of components
	mydevice = compconn.getstates(mydevice)
	
	for c in xrange(len(mydevice.comps)):
		for i in xrange(len(mydevice.comps[c].ios)):
			mydevice.comps[c].ios[i].state = compconn.getstates(mydevice.comps[c].ios[i])

	print "Push States"
	#(do this even if the rest above failed)
	#push those states to server
	servconn.pushstates(mydevice)
	


#END LOOP
print "End of Program"




