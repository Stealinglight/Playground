# This script pulls the latest Optics Camera Coverage data from Optics S3 and saves it to a local file
# To be used in the Optics Data Intake project to check for cameras that are not in Optics

import os

from opres_sdk.auth import get_isengard_boto3_session

# Set variables
bucket = "dcss-optics-camera-onboard-progress"
aws_account_id = "100886757055"
role_name = "OpticsCameraCoverageViewer"
prefix = "OpticsCameraCoverage-2023"


def find_latest_file(s3_client, prefix):
    response = s3_client.list_objects_v2(
        Bucket="dcss-optics-camera-onboard-progress", Prefix=prefix
    )
    if "Contents" in response:
        objs = sorted(response["Contents"], key=lambda obj: obj["LastModified"], reverse=True)
        return objs[0]["Key"]
    else:
        return None


def boto3_s3_pull(s3_client, key):
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read().decode("utf-8")
    return body


def get_optics_data():
    os.makedirs("CCReports", exist_ok=True)
    os.chdir("CCReports")
    session = get_isengard_boto3_session(
        aws_account_id="100886757055", role_name="OpticsCameraCoverageViewer"
    )
    s3_client = session.client("s3")
    key = find_latest_file(s3_client=s3_client, prefix=prefix)
    body = boto3_s3_pull(s3_client=s3_client, key=key)
    csv_file_name = os.path.basename(key)
    csv_file_path = f"{csv_file_name}.csv"
    csv_file = open(csv_file_path, "w")
    csv_file.write(body)
    return csv_file_path


def current_ccreport():
    os.makedirs("CCReports", exist_ok=True)
    os.chdir("CCReports")
    session = get_isengard_boto3_session(
        aws_account_id="942978847599", role_name="OpticsMetricsDashboard"
    )
    s3_client = session.client("s3")

    def latest_report(s3_client, prefix):  # Updated for pulling from OpSup S3
        response = s3_client.list_objects_v2(Bucket="optics-psas-camera-reports", Prefix=prefix)
        if "Contents" in response:
            objs = sorted(response["Contents"], key=lambda obj: obj["LastModified"], reverse=True)
            return objs[0]["Key"]
        else:
            return None

    key = latest_report(s3_client=s3_client, prefix=prefix)
    body = boto3_s3_pull(s3_client=s3_client, key=key)
    csv_file_name = os.path.basename(key)
    csv_file_path = f"{csv_file_name}.csv"
    csv_file = open(csv_file_path, "w")
    csv_file.write(body)
    return csv_file_path
