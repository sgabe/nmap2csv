#!/usr/bin/python

'''
Nmap2SS is a simple Python script to convert XML (-oX) Nmap or Masscan
output files to a single CSV spreadsheet which summarizes all hosts and open
ports in a table in IP,PORT1,PORT2,PORT3,...,PORTN format: The first row is
the header with all open ports found on the scanned hosts. In the following
rows the specified character (default X) marks if the given port was found
open on the given host. The script also generates per-target results which
includes version information, if it is available.
'''

__description__ = 'Nmap to CSV spreadsheet converter'
__author__ = 'Gabor Seljan'
__version__ = '0.2'
__date__ = '2015/12/06'

import os
import textwrap
import xml.etree.ElementTree as ET

from argparse import *

description = textwrap.dedent('''\
          _  _                 ___ ___ ___
         | \| |_ __  __ _ _ __|_  ) __/ __|
         | .` | '  \/ _` | '_ \/ /\__ \__ \\
         |_|\_|_|_|_\__,_| .__/___|___/___/
                         |_|

         Nmap to CSV spreadsheet converter
''')

parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description=description)

parser.add_argument('-i', metavar='INPUT', default='.', help='Scan output file or folder (default current folder)')
parser.add_argument('-p', metavar='PREFIX', default='nmap2ss', help='prefix for output file names (default nmap2ss)')
parser.add_argument('-s', metavar='SUFFIX', default='tcp', help='suffix for output file names (default tcp)')
parser.add_argument('-m', metavar='MARKER', default='X', help='marker character (default X)')

args = parser.parse_args()

FILES = []
ADDRS = []
PORTS = set()
RESULTS = {}
OUTPUT = []

if os.path.isdir(args.i):
  FILES = [os.path.join(args.i, f) for f in os.listdir(args.i) if f.endswith('.xml')]
elif os.path.isfile(args.i) and args.i.endswith('.xml'):
  FILES = [args.i]

if not FILES:
  parser.print_help()
  print('\n[-] No XML output file(s) found!')
  exit(1)

print(description)

for filename in FILES:
  root = ET.parse(filename).getroot()
  if root.get('scanner') == 'nmap':
    for host in root.findall('host'):
      if host.find('status').get('state') == 'up':
        addr = host.find('address').get('addr')
        if addr not in ADDRS:
          ADDRS.append(addr)
        for port in host.find('ports').findall('port'):
          if port.find('state').get('state') == 'open':
            portid = port.get('portid')
            PORTS.add(portid)
            if port.find('service') is not None:
              name = port.find('service').get('name')
              product = port.find('service').get('product')
              version = port.find('service').get('version')
            else:
              name = ''
              product = ''
              version = ''
            if addr in RESULTS:
              if portid not in RESULTS[addr].keys():
                RESULTS[addr][portid] = [name, product, version]
            else:
              RESULTS.update({addr : {portid : [name, product, version]}})
  else:
    for host in root.findall('host'):
      addr = host.find('address').get('addr')
      if addr not in ADDRS:
        ADDRS.append(addr)
      for port in host.find('ports').findall('port'):
        portid = port.get('portid')
        PORTS.add(portid)
        if addr in RESULTS:
          if portid not in RESULTS[addr].keys():
            RESULTS[addr][portid] = ['', '', '']
        else:
          RESULTS.update({addr : {portid : ['', '', '']}})

ADDRS = sorted(ADDRS, key=lambda x:tuple(map(int, x.split('.'))))
PORTS = sorted(PORTS, key=int)

print('[+] Found {} open ports on {} hosts!'.format(len(PORTS), len(ADDRS)))

if PORTS:
  output = ['0.0.0.0,' + ','.join(str(p) for p in PORTS)]
  for addr in ADDRS:
    row = addr + ','
    for portid in PORTS:
      try:
        if portid in RESULTS[addr].keys():
          row += args.m + ','
        else:
          row += ','
      except KeyError:
        pass
    output.append(row)

  with open('{}-summary-{}.csv'.format(args.p, args.s), 'w') as f:
    for row in output:
      f.write(row + '\n')
    print('[+] Summary results saved to {}'.format(f.name))

  for addr, ports in RESULTS.items():
    output = ['Port,Service,Product,Version']
    for port, info in sorted(ports.items(), key=lambda x:int(x[0])):
      row = '%s,%s' % (port, ','.join(map(str, info)))
      output.append(row)

    with open('{}-{}-{}.csv'.format(args.p, addr, args.s), 'w') as f:
      for row in output:
        f.write(row + '\n')
      print('[+] Per-target results saved to {}'.format(f.name))
