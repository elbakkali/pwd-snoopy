#!/usr/bin/env python3.8

import subprocess

result = subprocess.run(
    'grep -H ^psk= /etc/NetworkManager/system-connections/*', capture_output=True, text=True, shell=True
).stdout.strip().split('\n')

credentials = []

for val in result:
    val = list(filter(None, val.rsplit('/')))
    val = val[-1].split(':psk=')
    credentials.append({'ssid': val[0], 'password': val[1]})

print(credentials)
