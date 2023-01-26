import boto3

# First, assume a role in the first account
sts_client = boto3.client('sts')
response = sts_client.assume_role(
    RoleArn='arn:aws:iam::<ACCOUNT_1_ID>:role/<ROLE_NAME>',
    RoleSessionName='session1'
)
credentials = response['Credentials']

# Use the temporary credentials to access the first S3 bucket
s3_client = boto3.client('s3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)

# Download the object from the first S3 bucket
s3_client.download_file('<BUCKET_NAME>', '<OBJECT_KEY>', '/path/to/local/file')

# Assume a role in the second account
response = sts_client.assume_role(
    RoleArn='arn:aws:iam::<ACCOUNT_2_ID>:role/<ROLE_NAME>',
    RoleSessionName='session2'
)
credentials = response['Credentials']

# Use the temporary credentials to access the second S3 bucket
s3_client = boto3.client('s3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)

# Upload the object to the second S3 bucket
s3_client.upload_file('/path/to/local/file', '<BUCKET_NAME>', '<OBJECT_KEY>')

#################################

# Use Session to create a new S3 client that uses the cached session, 
# as I mentioned in my previous response, this can avoid the time consuming process
# of assuming a role and creating clients over and over again.


session = boto3.Session(
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)
s3_client = session.client('s3')

# You could move the repetitive code block of assuming a role, 
# creating a new s3_client and using it to access the S3 bucket into a function. 
# This way you can call the function twice, once for each account:

def access_s3_bucket(role_arn, role_session_name):
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )
    credentials = response['Credentials']
    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    s3_client = session.client('s3')
    return s3_client

# Call the function to access the first S3 bucket
s3_client = access_s3_bucket('arn:aws:iam::<ACCOUNT_1_ID>:role/<ROLE_NAME>', 'session1')

# Download the object from the first S3 bucket
s3_client.download_file('<BUCKET_NAME>', '<OBJECT_KEY>', '/path/to/local/file')

# Call the function to access the second S3 bucket
s3_client = access_s3_bucket('arn:aws:iam::<ACCOUNT_2_ID>:role/<ROLE_NAME>', 'session2')

# Upload the object to the second S3 bucket
s3_client.upload_file('/path/to/local/file', '<BUCKET_NAME>', '<OBJECT_KEY>')

# Provide visual feedback

# Print a message indicating that the script has completed
print("Object has been successfully downloaded from the first S3 bucket and uploaded to the second S3 bucket.")

try:
    # Call the function to access the first S3 bucket
    s3_client = access_s3_bucket('arn:aws:iam::<ACCOUNT_1_ID>:role/<ROLE_NAME>', 'session1')

    # Download the object from the first S3 bucket
    s3_client.download_file('<BUCKET_NAME>', '<OBJECT_KEY>', '/path/to/local/file')

    # Call the function to access the second S3 bucket
    s3_client = access_s3_bucket('arn:aws:iam::<ACCOUNT_2_ID>:role/<ROLE_NAME>', 'session2')

    # Upload the object to the second S3 bucket
    s3_client.upload_file('/path/to/local/file', '<BUCKET_NAME>', '<OBJECT_KEY>')

    # Print a message indicating that the script has completed
    print("Object has been successfully downloaded from the first S3 bucket and uploaded to the second S3 bucket.")
except Exception as e:
    print(f'Error occurred: {e}')

    # Print a message indicating that the script has failed
    print("Object could not be downloaded from the first S3 bucket and uploaded to the second S3 bucket.")