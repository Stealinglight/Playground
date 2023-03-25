import subprocess

def lambda_handler(event, context):
    command = event['body']['command']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = result.stdout.decode('utf-8')
    error = result.stderr.decode('utf-8')
    if error:
        raise Exception(error)
    return output
