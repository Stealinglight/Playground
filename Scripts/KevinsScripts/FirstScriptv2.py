import json
import re
import subprocess
import sim

def parse_ticket(json_response):
    data = json.loads(json_response)
    issue = data[0]
    title = issue["title"].decode()
    airport_code = re.search(r'\b[A-Z]{3}\b', title)
    desc = issue["description"]
    ip_address = re.search(r"10[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}", desc)
    return ip_address, airport_code

def ping_address(ip_address):
    reply = subprocess.run(['ping', '-c', '4', ip_address.group(0)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    nvr_online = reply.returncode == 0
    return nvr_online

def resolve_or_reassign(sim_client, issue_id, ping_results):
    message = f"{ping_results} replies with 0% packet loss, resolving."
    sim_client.add_comment(
            issue_id,
            message=message,
            content_type="text/plain"
            )
    sim_client.update_status(
            sim_id=issue_id, desired_status="Resolved", root_cause="DeviceHealthCheck"
            )

def main():
    sim_client = sim.Client()
    issues_folder = sim_client.get_issues_from_folder(folder_id="90d9c778-9cba-4c06-a74c-ef6f0c280ca1")
    issue = issues_folder[0]
    ip_address, airport_code = parse_ticket(issue)
    nvr_online = ping_address(ip_address)
    if nvr_online:
        resolve_or_reassign(sim_client, issue["id"], 4)

if __name__ == "__main__":
    main()
