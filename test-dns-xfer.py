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

parser = argparse.ArgumentParser(description="Test a domain for zone xfer" \
        ,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d","--domain",help="The domain you want record(s) for",default="example.org")
parser.add_argument("-o","--output",help="Output file to write to")
parser.add_argument("-v","--verbose",action="store_false",help="Verbose output")
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
            nameserver = dns.resolver.resolve(str(nameserver), rdtype=dns.rdatatype.A)
            the_xfer = dns.zone.from_xfr(dns.query.xfr(str(nameserver[0]), zonename))
            names = the_xfer.nodes.keys()
            for n in names:
                print(the_xfer[n].to_text(n))
                if args.output:
                    with open(args.output,'a+') as f:
                        f.write("DOMAIN: %s\n" % args.domain)
                        f.write(the_xfer[n].to_text(n))
    except dns.xfr.TransferError as e:
         print("ERR: %s" %e)

if __name__ == "__main__":
    get_zone_xfer(args.domain)
