#!/usr/bin/env python3.8

import subprocess

result = subprocess.run(
    'grep -H ^psk= /etc/NetworkManager/system-connections/*', capture_output=True, text=True, shell=True
).stdout.strip().split('\n')

ssids = []
passwords = []
credentials = []

for val in result:
    val = list(filter(None, val.rsplit('/')))
    val = val[-1].split(':psk=')
    ssids.append(val[0])
    passwords.append(val[1])
    credentials.append({'ssid': val[0], 'password': val[1]})

longestSsid = len(max(ssids, key=len))
longestpwd = len(max(passwords, key=len))

tableHeader = "SSID" + (" " * (longestSsid - len('SSUD') + 1)) + "| Password"
print(tableHeader)
print('-' * (longestSsid + longestpwd + 5))

for c in credentials:
    row = c['ssid'] + (' ' * (longestSsid - len(c['ssid']) + 1)) + '| ' + c['password']
    print(row)