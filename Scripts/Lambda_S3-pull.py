##Lambda function in Python to pull on object from S3 in another account 
##Then place it into another bucket

import boto3

def lambda_handler(event, context):
    # Assume a role in the other account
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn='arn:aws:iam::<ACCOUNT_1_ID>:role/<ROLE_NAME>',
        RoleSessionName='session1'
    )
    credentials = response['Credentials']

    # Use the temporary credentials to access the S3 bucket in the other account
    s3_client = boto3.client('s3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

    # Download the CSV file from the S3 bucket in the other account
    s3_client.download_file('<BUCKET_NAME>', '<OBJECT_KEY>', '/tmp/file.csv')

    # Use the default credentials of the Lambda function's role to access the S3 bucket in the same account
    s3_client = boto3.client('s3')

    # Upload the CSV file to the S3 bucket in the same account
    s3_client.upload_file('/tmp/file.csv', '<BUCKET_NAME>', '<OBJECT_KEY>')
