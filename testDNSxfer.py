#!/usr/bin/env python
'''

# Info: Query a supplied dns zone (or just a name without tld/gtld) for it's NS records and 
        test if it's offering transfers out to the world.

# Required: dnspython:
            sh-3.2$ pip install dnspython

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

socket.setdefaulttimeout(10)

'''
  Get NS records
'''
def getNameservers(zonename):
    try:
        nameservers = dns.resolver.query(zonename, 'NS') 
        return nameservers

        '''
        Catch exceptions
        '''
    except dns.resolver.NoNameservers:
        print("\nDomain:", zonename, "has no ns records, sorry ;(")
        return ""
    except dns.resolver.NXDOMAIN:
        print("\nNon-existent domain %s\n" % zonename)
        return ""
    except dns.exception.Timeout:
        print("\nTimeout\n")
        return ""
    except dns.resolver.NoAnswer: 
        print("\nproblem getting NS record\n")
        return ""

'''
  Check for and get required zone argument. Clean up the domain string if it contains anything other than
  the domain name
'''

def getArgs():
    if  len(sys.argv) != 2:
        print('\n     Usage: \n\n     %s  fqdn\n' % sys.argv[0])
        print('\n     Purpose: \n\n     Test a domain for open zone transfer\n')
        sys.exit(1)
    else:
        zonename=re.sub('https://|http://|www.','',sys.argv[1])
        zonename=zonename.split('/')
        print("ZONENAME: %s" %zonename[0])
        return zonename[0]

'''
  Try to transfer the zone
'''

def getZoneXfer(zonename):
    for nameserver in getNameservers(zonename):
        try:
            print('\nQuerying nameserver %s for DNS zone %s\nResult:\r' % (nameserver,zonename))

            tryxfer = dns.zone.from_xfr(dns.query.xfr(str(nameserver), zonename))
            names = tryxfer.nodes.keys()
            names.sort()
            f = open('/tmp/%s.%s.txt' %(zonename,str(nameserver)),'w')

            for n in names:
                 print(tryxfer[n].to_text(n))
                 f.write(tryxfer[n].to_text(n)+'\n')
            f.write('\nZone transferred from: ' + str(nameserver) + '\n')
            f.close()

        except dns.zone.NoNS:
            print("\nDomain: %s exists, but has no ns records, sorry ;( " %zonename)
        except dns.resolver.NXDOMAIN:
            print("\nDomain:", zonename, "unresponsive, try again\n")
        except dns.exception.FormError:
            print("\nXfer refused, good work dns admin\n")
        except EOFError:
            print("\nEOFError\n")
        except KeyboardInterrupt:
            print("\nUser cancelled\n")
        except KeyError as e: 
            print("KeyError %s" % e)
        except socket.error:
            print("\nFailed: connection refused\n")

zonename = getArgs()

'''
  If arg has no tld, let's append a few
'''

if string.find(zonename,'.') < 0:
    for tld in ('net','com','org','us','gov','info','co.uk','co.nz','it','pl','co.in','ly'):
        print("TLD %s" % tld)
        getZoneXfer("%s.%s"%(zonename,tld))
        #getZoneXfer(zonename + '.' + tld)
    sys.exit(0)

'''
  Get nameserver records
'''

try:
    ns = getNameservers(zonename)
    if ns:
        print("Number of NS records: %s" % len(ns))
        getZoneXfer(zonename)

except dns.resolver.NXDOMAIN:
    print("AAA Invalid name %s" % zonename)
    sys.exit(1)

except dns.exception.Timeout:
    print("\nAAATimeout while attempting to contact DNS server")
    sys.exit(1)
