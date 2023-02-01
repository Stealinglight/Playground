import json
import re
import subprocess

def parse_json(json_response):
    data = json.loads(json_response)
    title = data['title']
    description = data['description']
    
    try:
        airport_code = re.findall(r'\b[A-Z]{3}\b', title)[0]
        print(f'Airport code: {airport_code}')
    except IndexError:
        print("Airport code not found")
        return None
    
    try:
        ip_address = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', description)[0]
        print(f'IP address: {ip_address}')
        return ip_address
    except IndexError:
        print("IP address not found")
        return None


def ping_ip(ip):
    result = subprocess.run(['ping', '-c', '4', ip],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print(f'{ip} is reachable')
        close_ticket()
    else:
        print(f'{ip} is not reachable')
        reassign_ticket()


def close_ticket():
    print("Closing the ticket")


def reassign_ticket():
    print("Reassigning the ticket")

json_response = '{"title": "Airport ABC is down", "description": "The IP address of the server is 192.168.1.1"}'
ip_address = parse_json(json_response)

if ip_address:
    ping_ip(ip_address)
