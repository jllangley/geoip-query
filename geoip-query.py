import geoip2.database
import argparse
import socket
import sys
import re
reader = geoip2.database.Reader("/usr/local/lib/python2.7/dist-packages/_geoip_geolite2/GeoLite2-City.mmdb")

parser = argparse.ArgumentParser(description="Geoip lookup for IP addresses")
parser.add_argument('-f', metavar='file.csv', type=str, help='file with IP addresses comma seperated.')
parser.add_argument('-i', metavar='x.x.x.x', type=str, help='Insert IP address.')
args = parser.parse_args()

def ip_lookup_argv():
	try:
		match = reader.city(args.i)
		dnslookup = socket.gethostbyaddr(args.i)
		print (str(dnslookup)) + ", " +  (str(match.city.name)) + ", " +  (str(match.country.name)) + ", " +  (str(match.traits.user_type)) + ", " + (str(match.traits.domain))
	except socket.herror:
		print "unkown host" + ", " +  (str(match.city.name)) + ", " +  (str(match.country.name)) + ", " +  (str(match.traits.user_type)) + ", " + (str(match.traits.domain))
	except geoip2.errors.AddressNotFoundError:
		print "%s not in Database" % args.i
 
def ip_lookup_csv():
	with open(args.f) as txt_file:
		ip_read = txt_file.read()
		for ipaddr in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_read):
			match = reader.city(ipaddr)
			try:
				dnslookup = socket.gethostbyaddr(ipaddr)
				print (str(dnslookup)) + ", " +  (str(match.city.name)) + ", " +  (str(match.country.name)) + ", " +  (str(match.traits.user_type)) + ", " + (str(match.traits.domain))
			except socket.herror:
				print "unkown host" + ", " +  (str(match.city.name)) + ", " +  (str(match.country.name)) + ", " +  (str(match.traits.user_type)) + ", " + (str(match.traits.domain))
			except geoip2.errors.AddressNotFoundError:
				print "%s not in Database" % args.i
if args.f:
	print ip_lookup_csv()
elif args.i:
	print ip_lookup_argv()
else:
	print """
optional arguments:
  -h, --help   show this help message and exit
  -f file.csv  file with IP addresses comma seperated.
  -i x.x.x.x   Insert IP address."""

