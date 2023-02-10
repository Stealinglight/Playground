import requests
import base64

# Define the proxies
proxies = {
    "http": "http://<proxy_username>:<proxy_password>@<proxy1_ip>:<proxy1_port>",
    "https": "https://<proxy_username>:<proxy_password>@<proxy1_ip>:<proxy1_port>",
}

# Define the target URL
url = "http://<target_url>"

# Define the proxy credentials for the target URL
auth = requests.HTTPDigestAuth("<target_username>", "<target_password>")

# Send the request through the double hop proxy
response = requests.get(url, proxies=proxies, auth=auth)

# Check if the request was successful
if response.status_code == 200:
    print("Request was successful")
else:
    print("Request failed with status code:", response.status_code)


###########

import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the proxy server
ssh.connect('3.97.8.15', username='user', password='password')

# Create the proxy
transport = ssh.get_transport()
dest_addr = ('103.0.0.17', 22)
local_addr = ('127.0.0.1', 1234)
channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

# Use the proxy with requests library
proxies = {
  "http": "socks5://127.0.0.1:1234",
  "https": "socks5://127.0.0.1:1234",
}

url = f"http://{CAMERA_IP}/axis-cgi/opticssetup.cgi?autofocus=perform"
auth = requests.auth.HTTPDigestAuth(CAMERA_USERNAME, CAMERA_PASSWORD)
response = requests.get(url, auth=auth, proxies=proxies)

# Close the channel and the ssh connection
channel.close()
ssh.close()


###########

import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the first host
ssh.connect('3.97.8.15', username='your-username', password='your-password')

# Connect to the second host using the first host as a proxy
transport = ssh.get_transport()
destination_addr = ('103.0.0.17', 22)
local_addr = ('127.0.0.1', 1234)
channel = transport.open_channel("direct-tcpip", destination_addr, local_addr)

# Use Paramiko to create a second ssh client connected to the second host through the proxy
second_ssh = paramiko.SSHClient()
second_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
second_ssh.connect('103.0.0.17', username='your-username', password='your-password', sock=channel)


# Close the second transport
second_transport.close()

# Close the first transport
first_transport.close()
