#!/usr/bin/env python
'''

# Info: Query a supplied dns zone (or just a name without tld/gtld) for it's NS records and 
        test if it's offering transfers out to the world.

# Required: PyDNS, available here: http://pydns.sourceforge.net
            or via easy_install - eg: sh-3.2$ easy_install pydns

# Copyright (C) 2012
# Author: Beau Taub <beautaub@gmail.com>

# testDNSxfer is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# testDNSxfer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with testDNSxfer; see the file COPYING.  If not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA. 

'''

import dns.query, dns.zone, dns.resolver
import sys, socket, re, string

# Get NS records
def getNameservers(zonename):
    nameservers = dns.resolver.query(zonename, 'NS') 
    return nameservers

# Check for and get required zone argument. Clean up the domain string if it contains anything other than
# the domain name
def getArgs(zonename):
    if  len(sys.argv) != 2:
        print '\n     Usage: \n\n     {0}  fqdn\n'.format(sys.argv[0]) 
        print '\n     Purpose: \n\n     Test a domain for wide-open zone transfer\n'
        sys.exit(1)
    else:
        zonename=re.sub('https://|http://|www.','',sys.argv[1])
        zonename=zonename.split('/')
        return zonename[0]

def getZoneXfer(zonename):
    for nameserver in getNameservers(zonename):
        try:
            print '\nQuerying nameserver {0} for DNS zone {1}\nResult:\r'.format(nameserver,zonename)

            tryxfer = dns.zone.from_xfr(dns.query.xfr(str(nameserver), zonename))
            names = tryxfer.nodes.keys()
            names.sort()

            for n in names:
                 print tryxfer[n].to_text(n)

            sys.exit(0)

        except dns.resolver.NoAnswer: 
            print "\nproblem getting NS record\n"
        except dns.resolver.NXDOMAIN:
            print "\nDomain:", zonename, "unresponsive, try again\n"
        except dns.exception.FormError:
            print "\nXfer refused, good work dns admin\n"
        except dns.resolver.NoAnswer:
            print "\nNo Answer\n"
        except EOFError:
            print "\nEOFError\n"
        except KeyboardInterrupt:
            print "\nUser cancelled\n"
        except socket.error:
            print "\nFailed: connection refused\n"
        except dns.resolver.NoAnswer:
            print "\nInvalid Zone name\n"

zonename = ''
zonename = getArgs(zonename)

# If arg has no tld, let's append a few and see what's out there
if string.find(zonename,'.') < 0:
 #   print string.find(zonename,'m')
 #   print "no dot found"
    for tld in ('net','com','org'):
        getZoneXfer(zonename + '.' + tld)

socket.setdefaulttimeout(10)
#print "Socket timeout:", socket.getdefaulttimeout()

# Get nameserver records
try:
    ns = getNameservers(zonename)
    #if len(getNameservers(zonename)):
    if len(ns):
        print "Number of NS records:", len(ns)
        getZoneXfer(zonename)

except dns.resolver.NXDOMAIN:
    print "Invalid name" , zonename
    sys.exit(1)

except dns.resolver.NoAnswer:
    print "\nInvalid zone name: it's not a zone\n"
    sys.exit(1)

except dns.exception.Timeout:
    print "\nTimeout while attempting to contact DNS server"
    sys.exit(1)

