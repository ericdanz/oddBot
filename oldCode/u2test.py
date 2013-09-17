import urllib2, httplib


headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
		   
#Get latest action
url = "http://www.oddbotics.com/ui/d/10/ga"
req = urllib2.Request(url)
restring = urllib2.urlopen(req).read()
print restring
#split apart response to find action content
splitstring = restring.split('/')
split2 = splitstring[5].split(',')
io_id = split2[0]
action_content = split2[1]
action_id = split2[2]
url = "http://www.oddbotics.com/ui/d/10/ca/{}/{}".format(action_id, action_content)
print url
#confirm action
req = urllib2.Request(url)
restring = urllib2.urlopen(req).read()
print restring

#run action


#push new state
url = "http://www.oddbotics.com/ui/d/10/c/9/i/{}/ns/{}".format(io_id,action_content)

print url
req = urllib2.Request(url)
restring = urllib2.urlopen(req).read()
print restring




