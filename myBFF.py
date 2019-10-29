 
#! /usr/bin/python3

from argparse import ArgumentParser
import argparse
import sys
from modules import *

parser = ArgumentParser(description='my Brute Force Framework (myBFF)')
parser.add_argument('--service', '-s', nargs='?', required=True, help='Service to brute against (splunk, wordpress, sitescope, cisco, )')
parser.add_argument('--username', '-u', help='Username')
parser.add_argument('--userfile', '-U', help='Username File')
parser.add_argument('--password', '-p', help='Password')
parser.add_argument('--passfile', '-P', help='Password File')
parser.add_argument('--url', required=True, help='URL (Format: http://127.0.0.1:8000)')
parser.add_argument('--proxies', help='Comma-separated list of SOCKS proxies. (i.e., 127.0.0.1:9050,127.0.0.1:18085)')
parser.add_argument('--delay', '-d', default=60, help='Time delay (in seconds) between each password guess. (Used for password file only. Defaults to 60 seconds.)')

class myBFF:
    def run(self, args):
        url = args.url
        username = args.username
        password = args.password
        user_file = args.userfile
        pass_file = args.passfile
        delay = args.delay
        proxies = str(args.proxies).split(',')
        if args.service.lower() == 'splunk':
            splunk = splunkBrute.SplunkBrute()
            splunk.main(url, username, password, proxies, user_file, pass_file, delay)
        elif args.service.lower() == 'wordpress':
            wordpress = wordpressBrute.WPBrute()
            wordpress.main(url, username, password, proxies, user_file, pass_file, delay)
        elif args.service.lower() == 'sitescope':
            ss = SiteScopeBrute.SiteScopeBrute()
            ss.main(url, username, password, proxies, user_file, pass_file, delay)
        elif args.service.lower() == 'cisco':
            cisco = ciscoBrute.ciscoBrute()
            cisco.main(url, username, password, proxies, user_file, pass_file, delay)



    def asciiArt(self):
        print("""
                __________________ 
                | ___ \  ___|  ___|
 _ __ ___  _   _| |_/ / |_  | |_   
| '_ ` _ \| | | | ___ \  _| |  _|  
| | | | | | |_| | |_/ / |   | |    
|_| |_| |_|\__, \____/\_|   \_|    
            __/ |    v2.0              
           |___/                   
written by: l0gan (github.com/l0gan)
        """)


if __name__ == "__main__":
    args = parser.parse_args()
    myBFF().asciiArt()
    mybff = myBFF()
    mybff.run(args)
