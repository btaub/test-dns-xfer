#!/usr/bin/env python3

'''
# Required: dnspython:
sh-3.2$ pip install dnspython
'''
import dns.query
import dns.zone
import dns.resolver
import sys
import socket
import re
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Test a domain for zone transfer" \
        ,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d","--domain",help="The domain you want record(s) for",default="example.org",required=True)
parser.add_argument("-o","--output",help="Create output file for transfer", action="store_true")
parser.add_argument("-v","--verbose",action="store_true",help="Verbose output")
args = parser.parse_args()

def get_nameservers(zonename):
    try:
        nameservers = dns.resolver.resolve(zonename, 'NS')
        return(nameservers)
    except Exception as e:
        print("%s" %(e))
        return

def get_zone_xfer(zonename):
    for nameserver in get_nameservers(zonename):
        if args.verbose:
            print("[+] Testing nameserver: %s" % (nameserver))
        nameserver_ip = dns.resolver.resolve(str(nameserver), rdtype=dns.rdatatype.A)
        try:
            the_xfer = dns.zone.from_xfr(dns.query.xfr(str(nameserver_ip[0]), zonename))
            names = the_xfer.nodes.keys()
            for n in names:
                if args.output:
                    ts = datetime.now().strftime("%Y%d%m-%I%M")
                    with open(args.domain+"-"+str(nameserver)+ts+".txt",'a+') as f:
                        f.write("DOMAIN: %s\n" % args.domain)
                        f.write(the_xfer[n].to_text(n))
                if args.verbose:
                    print(the_xfer[n].to_text(n))
            print("Transfer from nameserver %s successful, check output for details if -o was specified" % nameserver)

        except Exception as e:
            print("[x] %s: %s" %(nameserver, e))

if __name__ == "__main__":
    try:
        get_zone_xfer(args.domain)
    except Exception as e:
        if args.verbose:
            print("%s" %(e))
