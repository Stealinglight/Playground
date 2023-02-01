## Camera Pinger ##
# Create a list of IP Addresses to ping 
# You can copy and paste a list or type row by row
# The script will ping each IP address and print the results
# If module error 
# python3 -m pip install tqdm

import subprocess
import socket
from tqdm import tqdm

ip_addresses = []

# Check if the input is a list or line by line
while True:
    ip_address = input("\nEnter an IP address per line or 'end' to stop: ")
    if ip_address == 'end' or ip_address == '':
        break

    for address in ip_address.splitlines():
        try:
            socket.inet_aton(address)
            ip_addresses.append(address)
        except socket.error:
            print(f'Error: {address} is not a valid IP address.')

# Ping each IP address in the list
for ip_address in tqdm(ip_addresses, desc='Pinging IP Addresses'):
    reply = subprocess.run(['ping', '-c', '4', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if reply.returncode == 0:
        print(f'\033[32m \nCamera {ip_address} is online.\033[0m\n{reply.stdout.decode()}')
    else:
        print(f'\033[31m \nCamera {ip_address} is unreachable.\033[0m\n{reply.stderr.decode()}')

print('\nFinished\n')


