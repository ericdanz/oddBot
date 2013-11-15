import sys
import bluetooth

muuid = "insecure"
service_matches = bluetooth.find_service(uuid = muuid)

in len(service_matches) == 0:
	print "No matches for insecure"
	sys.exit(0)
	
for match in service_matches:
	print "{name} {port} {host}".format(*match)

muuid = "secure"
service_matches = bluetooth.find_service(uuid = muuid)

in len(service_matches) == 0:
	print "No matches for secure"
	sys.exit(0)
	
for match in service_matches:
	print "{name} {port} {host}".format(*match)
