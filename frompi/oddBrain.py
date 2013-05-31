import urllib2,httplib

conn =  urllib2.urlopen('http://www.oddbotics.com/ui/d/10/ga')
nextAction = conn.read()
if nextAction != 'No New Actions':
	naSplit = nextAction.split(',')
	print naSplit[0]
	confurlstring =  'http://www.oddbotics.com/ui/d/10/ca/{}/{}'.format(naSplit[2], naSplit[1])
	print confurlstring
	confconn = urllib2.urlopen(confurlstring)
	print confconn.read()


	pushStateUrl = 'http://www.oddbotics.com/ui/{}/ns/{}'.format(naSplit[0],naSplit[1])
	print pushStateUrl
	psconn = urllib2.urlopen(pushStateUrl)
	print psconn.read()
else:
	print 'Nothin New'
