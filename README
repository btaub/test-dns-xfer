# test-dns-xfer
This script tests whether or not a domain allows [zone transfers](https://en.wikipedia.org/wiki/DNS_zone_transfer)

## Sample usage
```
$ ./test-dns-xfer.py -h
usage: test-dns-xfer.py [-h] -d DOMAIN [-o] [-v]

Test a domain for zone transfer

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        The domain you want record(s) for (default: example.org)
  -o, --output          Create output file for transfer (default: False)
  -v, --verbose         Verbose output (default: False)
```

## Zone transfers disallowed/disabled:
$ ./test-dns-xfer.py -d example.com
[x] b.iana-servers.net.: Zone transfer error: REFUSED
[x] a.iana-servers.net.: Zone transfer error: NOTAUTH

## Zone tranfers enabled
$ ./test-dns-xfer.py -d churchofherpetology.org
Transfer from nameserver ns1.access.net. successful, check output for details if -o was specified
Transfer from nameserver ns2.access.net. successful, check output for details if -o was specified

## Zone transfer enabled, verbose output
$ ./test-dns-xfer.py -v -d churchofherpetology.org
[+] Testing nameserver: ns2.access.net.
@ 86400 IN SOA ns2.access.net. hostmaster.access.net. 2022061000 3600 300 3600000 900
@ 86400 IN NS ns1.access.net.
@ 86400 IN NS ns2.access.net.
@ 86400 IN MX 100 custmx.panix.com.
@ 86400 IN A 166.84.8.241
@ 86400 IN TXT "v=spf1 include:custspf.panix.com ?all"
autoconfig 86400 IN CNAME autoconfig.panix.com.
autodiscover 86400 IN CNAME autodiscover.panix.com.
www 86400 IN A 166.84.8.241
Transfer from nameserver ns2.access.net. successful, check output for details if -o was specified
[+] Testing nameserver: ns1.access.net.
@ 86400 IN SOA ns2.access.net. hostmaster.access.net. 2022061000 3600 300 3600000 900
@ 86400 IN NS ns1.access.net.
@ 86400 IN NS ns2.access.net.
@ 86400 IN MX 100 custmx.panix.com.
@ 86400 IN A 166.84.8.241
@ 86400 IN TXT "v=spf1 include:custspf.panix.com ?all"
autoconfig 86400 IN CNAME autoconfig.panix.com.
autodiscover 86400 IN CNAME autodiscover.panix.com.
www 86400 IN A 166.84.8.241
Transfer from nameserver ns1.access.net. successful, check output for details if -o was specified

--
<sub>Copyleft 2022, all rights reversed.</sub>
