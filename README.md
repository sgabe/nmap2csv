Nmap2SS
=======

**Nmap2SS** is a simple Python script to convert one or more normal (`-oN`) Nmap output files to a single CSV spreadsheet which summarizes all hosts and open ports in a table in `IP,PORT1,PORT2,PORT3,...,PORTN` format: The first row is the header with all open ports found on the scanned hosts. In the following rows the specified character (default `X`) marks if the given port was found open on the given host.

## Usage

Pass the normal Nmap output (`-oN`) via a specified file or directory (`-i`). The resulted CSV spreadsheet is saved to a file (default is spreadsheet.csv) and can also be displayed on the console (`-v`).

### Options
```
$ python nmap2ss.py -h
usage: nmap2ss.py [-h] [-i INPUT] [-o OUTPUT] [-m MARKER] [-v]

 _  _                 ___ ___ ___
| \| |_ __  __ _ _ __|_  ) __/ __|
| .` | '  \/ _` | '_ \/ /\__ \__ \
|_|\_|_|_|_\__,_| .__/___|___/___/
                |_|

Nmap to CSV spreadsheet converter

optional arguments:
  -h, --help  show this help message and exit
  -i INPUT    Nmap output file or folder (default current folder)
  -o OUTPUT   CSV output filename (default spreadsheet.csv)
  -m MARKER   marker character (default X)
  -v          display output on console
```

### Example output
```
0.0.0.0,123,135,139,443,445,
192.168.1.1,,X,X,,,
192.168.1.2,X,,,X,X,
192.168.1.3,X,,,,,
192.168.1.4,,,,X,X,
```
| 0.0.0.0     | 123 | 135 | 139 | 443 | 445 |
| ------------|:---:|:---:|:---:|:---:|:---:|
| 192.168.1.1 |     |  X  |  X  |     |     |
| 192.168.1.2 |  X  |     |     |  X  |  X  |
| 192.168.1.3 |  X  |     |     |     |     |
| 192.168.1.4 |     |     |     |  X  |  X  |

## License
This project is licensed under the terms of the MIT license.
