#! /usr/bin/python
import random


class proxySelector:
    def proxySelect(self, proxies):
        proxy = random.choice(proxies)
        print("[!] Proxying through " + proxy)
        proxy = {   'http': 'socks5://' + proxy,
                    'https': 'socks5://' + proxy
        }
        return proxy