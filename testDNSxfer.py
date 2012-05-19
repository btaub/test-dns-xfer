#!/usr/bin/env python
'''

# Info: testDNSxfer.py - Query a supplied dns zone for it's NS records and 
                         test if it's offering transfers out to the world.
                         Basicall, this script automates a couple dig commands:
                             dig -tns example.org
                             dig @ns1.example.org axfr
                             dig @ns2.... etc.

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

import dns.query, dns.zone, dns.resolver, sys, socket

# Get NS records
def getNameservers(zonename):
    nameservers = dns.resolver.query(zonename, 'NS') 
    return nameservers

# Check for and get required zone argument
def getArgs(zonename):
    if  len(sys.argv) != 2:
        print '\n     Usage: \n\n     {0}  fqdn\n'.format(sys.argv[0]) 
        print '\n     Purpose: \n\n     Test a domain for wide-open zone transfer\n'
              
        sys.exit(1)
    else:
        return sys.argv[1]

zonename = ''
zonename = getArgs(zonename)

# Get nameserver records
try:
    ns = getNameservers(zonename)
    #if len(getNameservers(zonename)):
    if len(ns):
        print "Number of NS records:", len(ns)

except dns.resolver.NXDOMAIN:
    print "Invalid name" , zonename
    sys.exit(1)

except dns.resolver.NoAnswer:
    print "\nInvalid zone name: it's not a zone\n"
    sys.exit(1)

# Attempt to transfer the zone from each nameserver, stop if 1 server gives up the zone 
for nameserver in getNameservers(zonename):
    try:

        print '\n   - Querying nameserver {0} for DNS zone {1}\n'.format(nameserver,zonename)

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