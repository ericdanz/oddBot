import urllib2, httplib, urllib
import deviceclass

def getaction(device_id):
	url = "http://www.oddbotics.com/ui/d/{}/ga".format(device_id)
	req = urllib2.Request(url)
	restring = urllib2.urlopen(req).read()
	#check to see if its a null response
	if (restring == "No New Actions"):
		return 0
	else:
		#split apart response to find action content
		splitstring = restring.split('/')
		split2 = splitstring[5].split(',')
		action = deviceclass.thing()
		action.content = int(split2[1])
		action.id = int(split2[2])
		action.actori = int(split2[0])
		action.actorc = int(splitstring[3])
		return action
	

def confaction(action):
	url = "http://www.oddbotics.com/ui/d/10/ca/{}/{}".format(action.id, action.content)
	req = urllib2.Request(url)
	restring = urllib2.urlopen(req).read()
	return restring
	
	
def pushastate(io_id, io_state, component_id):
	#push a single state
	url = "http://www.oddbotics.com/ui/d/10/c/{}/i/{}/ns/{}".format(component_id,io_id,io_state)
	try:
		req = urllib2.Request(url)
		restring = urllib2.urlopen(req).read()
	except urllib2.HTTPError, e:
		restring = 'error'
	return restring

def pushstates(adevice):
	#push all states
	#declare a null restring in case there are no ios in components
	restring = "no ios"
	for c in xrange(len(adevice.comps)):
		for i in xrange(len(adevice.comps[c].ios)):
			restring = pushastate(i,adevice.comps[c].ios[i].state,adevice.comps[c].compid)
	return restring
	
def pushconfig(adevice):
	url = "http://www.oddbotics.com/ui/d/{}/setup".format(adevice.id)
	hrs = {'Connection': 'close', 'Accept-Encoding': 'none', "Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"}
	params = {}
	cx = 0
	for c in adevice.comps:
		params.update({"component{}id".format(cx): c.compid})
		params.update({"component{}port".format(cx): c.port})
		ix = 0
		for i in c.ios:
			params.update({"{}io{}classOf".format(cx,ix):i.classOf, "{}io{}typeOf".format(cx,ix):i.typeOf,"{}io{}lowerBound".format(cx,ix):i.lowerBound,"{}io{}upperBound".format(cx,ix):i.upperBound,"{}io{}granularity".format(cx,ix):i.granularity,"{}io{}isInput".format(cx,ix):i.isInput})
		
	data = urllib.urlencode(params)
	url = "{}?{}".format(url,data)
	print "This is what I'm trying to upload: {}".format(url)
	req = urllib2.Request(url)
	try:
		response = urllib2.urlopen(req)
		restring = response.read()
	except urllib2.HTTPError, e:
			#if e.code == 500:
			#	response = urllib2.urlopen(req)
			#print e.code()
			restring = 'error'
			#print e.read()
	
	return restring