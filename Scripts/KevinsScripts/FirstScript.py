import opres_sdk
from opres_sdk import sim
import re
import os
import subprocess
import json




## Still needs to be fixed #
# Defining the Ticket Parser function to find the IP address in the ticket
def parse_ticket(json_response):
    data = json.loads(json_response)
    issue = issues_folder[0]
    title = issue.title.decode()
    airport_code = re.search(r'\b[A-Z]{3}\b', title)
    desc = issue.data["description"]
    ip_address = re.search(r"10[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}", desc)
    return issue, title, desc, ip_address, airport_code

# Defining the Ping function to ping the IP address found in the ticket
def ping_address(ip_address):
    reply = subprocess.run(['ping', '-c', '4', address.group(0)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if reply.returncode == 0:
        nvr_online = True            
    else:
        nvr_online = False               
    ping_results = reply
    return nvr_online, ping_results

## This is a mess and needs to be fixed #
# Defining the function to add a comment to the ticket based on the ping results
def resolve_or_reassign(sim_client, issue_id):
    sim_client.add_comment(
            issue_id,
            message = print(f"{ping_results} replies with 0% packet loss, resolving."),
            content_type = CONTENT_TYPE_TEXT,
            )
    sim_client.update_status(
            sim_id = sim_id, desired_status = "Resolved", root_cause = "DeviceHealthCheck"
            )
    return print(f"Ticket ")


# Defining Variables
sim_client = sim.Client()
issues_folder = sim_client.get_issues_from_folder(folder_id="90d9c778-9cba-4c06-a74c-ef6f0c280ca1")
# result = "V796073191" # This for testing purposes only
issue = sim_client.get_issue(issue_id=issues_folder[0])
address, issue, title, desc = parse_ticket(sim_client, issues_folder)
nvr_online, ping_results = ping_address(address)
issue_id = issue.id
sim_id = issue.sim_id
CONTENT_TYPE_TEXT = "text/plain"






