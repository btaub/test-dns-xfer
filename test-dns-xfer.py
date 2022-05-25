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

parser = argparse.ArgumentParser(description="Test a domain for zone xfer" \
        ,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d","--domain",help="The domain you want record(s) for",default="example.org")
parser.add_argument("-o","--output",help="Create output file for transfer", action="store_true")
parser.add_argument("-v","--verbose",action="store_true",help="Verbose output")
args = parser.parse_args()

def get_nameservers(zonename):
    try:
        nameservers = dns.resolver.resolve(zonename, 'NS')
        return(nameservers)
    except dns.resolver.NoNameservers as e:
        print("ERR: %s" %e)
    except dns.resolver.NXDOMAIN as e:
        print("ERR: %s" %e)
        return

def get_zone_xfer(zonename):
    try:
        for nameserver in get_nameservers(zonename):
            if args.verbose:
                print("[+] Testing nameserver: %s" % (nameserver))
            nameserver_ip = dns.resolver.resolve(str(nameserver), rdtype=dns.rdatatype.A)
            the_xfer = dns.zone.from_xfr(dns.query.xfr(str(nameserver_ip[0]), zonename))
            names = the_xfer.nodes.keys()
            for n in names:
               if args.output:
                   ts = datetime.now().strftime("%d%m%Y-%I%M%s")
                   with open(args.domain+"-"+str(nameserver)+ts+".txt",'a+') as f:
                        f.write("DOMAIN: %s\n" % args.domain)
                        f.write(the_xfer[n].to_text(n))
                   if args.verbose:
                        print(the_xfer[n].to_text(n))

            print("Transfer from nameserver %s successful, check output log for details" % nameserver)

    except dns.xfr.TransferError as e:
         print("ERR: %s" %e)

if __name__ == "__main__":
    get_zone_xfer(args.domain)
