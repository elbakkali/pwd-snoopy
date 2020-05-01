#!/usr/bin/env python3.8

import subprocess
import platform
import os

ssids = []
passwords = []
credentials = []
osName = platform.system()
result = None

if osName == 'Linux':
    if os.geteuid() != 0:
        exit('This script needs root privilages, please re-execute as root.')
        
    result = subprocess.run(
        'grep -H ^psk= /etc/NetworkManager/system-connections/*', capture_output=True, text=True, shell=True
    ).stdout.strip().split('\n')
    
    for val in result:
        val = list(filter(None, val.rsplit('/')))
        val = val[-1].split(':psk=')
        ssids.append(val[0])
        passwords.append(val[1])
        credentials.append({'ssid': val[0], 'password': val[1]})

elif osName == 'Windows':
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
    ssids = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

    for i in ssids:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
        pwd = [b.split(":")[1][1:-1] for b in data if "Key Content" in b][0]
        passwords.append(pwd)
        credentials.append({'ssid': i, 'password': pwd})

else:
    exit('This os is currently not supported.')

if not credentials:
    exit('There are currently no saved WIFI passwords saved on this machine.')

longestSsid = len(max(ssids, key=len))
longestpwd = len(max(passwords, key=len))
tableHeader = "SSID" + (" " * (longestSsid - len('SSUD') + 1)) + "| Password"

print(tableHeader)
print('-' * (longestSsid + longestpwd + 5))

for c in credentials:
    row = c['ssid'] + (' ' * (longestSsid - len(c['ssid']) + 1)) + '| ' + c['password']
    print(row)