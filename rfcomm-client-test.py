import sys
import bluetooth

muuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"
service_matches = bluetooth.find_service(uuid = muuid)

in len(service_matches) == 0:
	print "No matches for insecure"
	sys.exit(0)
	
for match in service_matches:
	print "{name} {port} {host}".format(*match)

muuid = "fa87c0d0-afac-11de-8a39-0800200c9a66"
service_matches = bluetooth.find_service(uuid = muuid)

in len(service_matches) == 0:
	print "No matches for secure"
	sys.exit(0)
	
for match in service_matches:
	print "{name} {port} {host}".format(*match)
