#!/usr/bin/python

'''
Nmap2SS is a simple Python script to convert one or more normal (-oN) Nmap
output files to a single CSV spreadsheet which summarizes all hosts and open
ports in a table in IP,PORT1,PORT2,PORT3,...,PORTN format: The first row is
the header with all open ports found on the scanned hosts. In the following
rows the specified character (default X) marks if the given port was found
open on the given host.
'''

__description__ = 'Nmap to CSV spreadsheet converter'
__author__ = 'Gabor Seljan'
__version__ = '0.1'
__date__ = '2014/12/07'

import os, re, textwrap
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

parser.add_argument('-i', metavar='INPUT', default='.', help='Nmap output file or folder (default current folder)')
parser.add_argument('-o', metavar='OUTPUT', default='spreadsheet', help='CSV output filename (default spreadsheet.csv)')
parser.add_argument('-m', metavar='MARKER', default='X', help='marker character (default X)')
parser.add_argument('-v', action='store_true', help='display output on console')

args = parser.parse_args()

FILES = []
IPS = []
PORTS = []
RESULTS = {}
OUTPUT = []

if os.path.isdir(args.i):
  FILES = [os.path.join(args.i, f) for f in os.listdir(args.i) if f.endswith('.nmap')]
elif os.path.isfile(args.i) and args.i.endswith('.nmap'):
  FILES = [args.i]

if not FILES:
  parser.print_help()
  print('\n[-] No *.nmap output file found!')
  exit()

print(description)

for filename in FILES:
  with open(filename, 'r') as f:
    text = f.read()
    for i in re.compile('^Nmap scan report for ', re.M).split(text):
      m = re.search('[\(]?(\d+\.\d+\.\d+\.\d+)[\)]?$', i, re.M)
      if m:
        ip = m.group(1)
        if ip not in IPS:
          IPS.append(ip)
        ports = re.findall('^(\d+)\/.*\sopen\s.*$', i, re.M)
        PORTS += ports
        RESULTS.update({ip : ports})

PORTS = sorted(set(PORTS), key=int)

print('[+] Found {} open ports on {} hosts!'.format(len(PORTS), len(IPS)))

if PORTS:
  OUTPUT.append('0.0.0.0,' + ','.join(PORTS))
  for ip in sorted(IPS, key=lambda x:tuple(map(int, x.split('.')))):
    row = ip + ','
    for port in PORTS:
      if port in RESULTS[ip]:
        row += args.m + ','
      else:
        row += ','
    OUTPUT.append(row)

  with open(args.o + '.csv', 'w') as f:
    for row in OUTPUT:
      f.write(row + '\n')
      if args.v:
        print(row)

  print('[+] Results saved to {}.csv!\n'.format(args.o))
