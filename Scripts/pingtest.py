import subprocess

ip_address = input("What IP would you like to ping? ")

reply = subprocess.run(['ping', '-c', '4', '-n', ip_address])

if reply.returncode == 0:
    online = True
    print(reply)
    
else:
    online = False
    print('Unreachable')

#testing output
print(online)