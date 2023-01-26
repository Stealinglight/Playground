# How can I create a script in Python that will parse a JSON response from sim.client 
# and find an airport code in the title and an IP address in the description of the JSON response.
# Then take the ip address and ping it 4 times, If there's a response it will close the ticket,
# If there's no response from the ping it will reassign the ticket 

import json
import re
import subprocess

# Function to parse the JSON response and find the airport code and IP address
def parse_json(json_response):
    # Load the JSON response into a Python dictionary
    data = json.loads(json_response)

    # Extract the title and description from the JSON response
    title = data['title']
    description = data['description']

    # Use regular expressions to find the airport code in the title
    airport_code = re.search(r'\b[A-Z]{3}\b', title).group()
    print(f'Airport code: {airport_code}')

    # Use regular expressions to find the IP address in the description
    ip_address = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', description).group()
    print(f'IP address: {ip_address}')
    return ip_address

def ping_ip(ip):
    # Use the `ping` command to send 4 pings to the IP address
    result = subprocess.run(['ping', '-c', '4', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        # If the ping command returns a 0 exit code, it means that the IP address is reachable
        print(f'{ip} is reachable')
        # close the ticket 
        close_ticket()
    else:
        # If the ping command returns a non-zero exit code, it means that the IP address is not reachable
        print(f'{ip} is not reachable')
        # Reassign the ticket 
        reassign_ticket()

def close_ticket():
    print("Closing the ticket")
    # code to close the ticket

def reassign_ticket():
    print("Reassigning the ticket")
    # code to reassign the ticket

# Example JSON response
json_response = '{"title": "Airport ABC is down", "description": "The IP address of the server is 192.168.1.1"}'

# Parse the JSON response and find the airport code and IP address
ip_address = parse_json(json_response)
# ping the ip address
ping_ip(ip_address)

# Here are a few ways you can refine the code to work better:

# Instead of using regular expressions to find the airport code and IP address, 
# you can use the json module's built-in functionality to extract the values you're looking for. 
# This would make the code more readable and easier to maintain.

# Add error handling to the code to handle cases where the airport code or IP address is not found in the JSON response. 
# You can use the try and except statements to catch any exceptions that might be thrown when the regular expressions fail to match.

# You can use the subprocess.run() function to check if the ping command has been successful or not, 
# as it returns a CompletedProcess object, which has a returncode attribute. 
# Using returncode is more readable and reliable than comparing the output of the command to a string.

# Instead of hardcoding the command, 
# you can create a variable to hold the command 
# and its arguments, and then pass it to subprocess.run()

# You can also abstract the code to ping the IP address into a function, 
# so it can be reused in other parts of your code.

# If you are going to use this script in a production environment, 
# you should also consider adding a mechanism for retrying the ping command in case of failure, 
# and also adding a timeout for the ping command.



import json
import subprocess

def parse_json(json_response):
    data = json.loads(json_response)
    title = data.get('title', '')
    description = data.get('description', '')
    airport_code = title.split()[1]
    ip_address = description.split()[-1]
    return airport_code, ip_address

def ping_ip(ip_address):
    command = ['ping', '-c', '4', ip_address]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
