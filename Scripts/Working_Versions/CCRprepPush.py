#CCRprepPush.py
#CameraCoverageReport prep and push script
# The purpose of this script is to validate the CSV file that is pulled from Optics Camera Coverage Report

import os
import re

import DataChecker
import isengard  # type: ignore
import pandas as pd
from OpticsDataPull import get_optics_data


def opccr_prep_clean(df):
    df = DataChecker.opticsccrprep(df)  # 0. Prep the data for analysis and parsing
    df = DataChecker.headercheck(df)  # 1. Check if the header is correct
    df = DataChecker.site_uc_zero_checker(
        df
    )  # 2. Checks if Building is present, Corrects "uc_" and '0' errors
    df = DataChecker.nte_filter_out(df)  # 3. Filter out NTE sites and validate IPs
    df = DataChecker.networkfabriccheck(df)  # 4. Assigns Network Fabric
    df = DataChecker.camnameclean(
        df
    )  # 5. Check if the camera name is valid fixes white spaces and fixes extra columns removes special characters
    return df  # Returns DataFrame ready for deploying to Optics


def pushddbucket(new_file_path):
    client = isengard.Client()
    session = client.get_boto3_session("S3BUCKET", "OpticsMetricsDashboard")
    s3 = session.client("s3")
    s3.upload_file(new_file_path, "optics-daily-deployment", new_file_path)
    return print(f"{new_file_path} uploaded to S3 bucket")


def clusterparser(new_file_path, df):
    dir_name = os.path.dirname("./CCReports")
    for building_code in df["Building"].str.slice(stop=3).unique():
        building_df = df[df["Building"].str.slice(stop=3) == building_code]
        # check if more than 500 rows
        if len(building_df) > 500:
            filename = f"{building_code} Optics Cameras Part 1.csv"
            building_df.iloc[:500].to_csv(
                os.path.join(os.path.dirname(new_file_path), filename), index=False
            )
            pushddbucket(os.path.join(os.path.dirname(new_file_path), filename))
            building_df = building_df.iloc[500:]
            if len(building_df) > 500:
                filename = f"{building_code} Optics Cameras Part 2.csv"
                building_df.iloc[:500].to_csv(
                    os.path.join(os.path.dirname(new_file_path), filename), index=False
                )
                pushddbucket(os.path.join(os.path.dirname(new_file_path), filename))
                building_df = building_df.iloc[500:]
                filename = f"{building_code} Optics Cameras Part 3.csv"
                building_df.to_csv(
                    os.path.join(os.path.dirname(new_file_path), filename), index=False
                )
                pushddbucket(os.path.join(os.path.dirname(new_file_path), filename))
            else:
                filename = f"{building_code} Optics Cameras Part 2.csv"
                building_df.to_csv(
                    os.path.join(os.path.dirname(new_file_path), filename), index=False
                )
                pushddbucket(os.path.join(os.path.dirname(new_file_path), filename))
        else:
            filename = f"{building_code} Optics Cameras.csv"
            building_df.to_csv(os.path.join(os.path.dirname(new_file_path), filename), index=False)
            pushddbucket(os.path.join(os.path.dirname(new_file_path), filename))

    print(f"Files saved to directory {dir_name}")


def folder_cleanup():
    if os.path.isdir("."):
        for filename in os.listdir("."):
            if filename.endswith(".csv"):
                os.remove(os.path.join(".", filename))
    else:
        path = os.path.join(os.getcwd(), "optics_data_intake", "CCReports")
        if os.path.isdir(path):
            os.chdir(path)
            for filename in os.listdir("."):
                if filename.endswith(".csv"):
                    os.remove(os.path.join(".", filename))
        else:
            print("Directory 'CCReports' not found")
            return
    print("Folder cleaned up")


# Print out the first 5 rows of the DataFrame for testing
# print(df.head()) # Uncomment to test


def save_to_csv(df, opcsv):
    match = re.search(r"\d{4}-\d{2}-\d{2}", os.path.basename(opcsv))
    if match:
        date_str = match.group(0)
        new_file_name = f"OpticsCameraCoverage-{date_str}.csv"
        new_file_path = os.path.join(os.path.dirname(opcsv), new_file_name)
        df.to_csv(new_file_path, index=False)
        print(f"{new_file_path} save to CCReports folder")
    else:
        print("Error: could not find date in file name.")
    return opcsv


def upload_backup(df, opcsv):
    match = re.search(r"\d{4}-\d{2}-\d{2}", os.path.basename(opcsv))
    if match:
        date_str = match.group(0)
        new_file_name = f"OpticsCameraCoverage-{date_str}.csv"
        new_file_path = os.path.join(os.path.dirname(opcsv), new_file_name)
        df.to_csv(new_file_path, index=False)
        client = isengard.Client()
        session = client.get_boto3_session("S3BUCKET", "OpticsMetricsDashboard")
        s3 = session.client("s3")
        s3.upload_file(new_file_path, "optics-psas-camera-reports", new_file_path)
        print(f"{new_file_path} uploaded to optics-psas-camera-reports S3 bucket")
    else:
        print("Error: could not find date in file name.")
    return df


# Save the DataFrame to a CSV file and to upload in OpSup S3
def csv_pd(opcsv):
    with open(opcsv, "r") as file:
        df = pd.read_csv(file, header=0, encoding="utf-8", usecols=range(18), error_bad_lines=False, low_memory=False)  # type: ignore
    df = DataChecker.removedups(df)  # Remove duplicates
    df = upload_backup(df, opcsv)  # Pass opcsv as a parameter
    return df


# Main function
def ccrprepnpush():
    opcsv = get_optics_data()
    df = csv_pd(opcsv)
    df = opccr_prep_clean(df)
    new_csv = save_to_csv(df, opcsv)  # Pass opcsv as a parameter
    clusterparser(new_csv, df)
    folder_cleanup()


def lamb_trigger(event, context):
    ccrprepnpush()
    return {"message": "Successful Job completed for report date: {date_str}"}


if __name__ == "__main__":
    ccrprepnpush()

# Deploy_Batches.py
from Algalon_Clusters import Cluster_codes
import pandas as pd
import os
import re
import algalon
import csv
import uuid
import isengard

bucket = 'optics-daily-deployment'
client = isengard.Client()
session = client.get_boto3_session("BUCKET", "OpticsMetricsDashboard")
s3 = session.client("s3")
deployment_batch = []
cameras_deployed = 0


def PullClusterCSV(s3_key):
    client = isengard.Client()
    session = client.get_boto3_session("BUCKET", "OpticsMetricsDashboard")
    s3 = session.client("s3")
    s3.download_file("optics-daily-deployment", s3_key, s3_key)
    print(f"{s3_key} found and downloaded to be processed")
    s3.delete_object(Bucket="optics-daily-deployment", Key=s3_key)
    return s3_key

def process_s3_folder(bucket, cluster_codes):
    os.makedirs('scripts/Failed_camData', exist_ok=True)
    os.chdir('scripts/Failed_camData')
    response = s3.list_objects_v2(Bucket=bucket)
    for obj in response.get('Contents', []):
        key = obj['Key']
        match = re.search(r'^([A-Z]{3})', key)
        if match:
            realm = match.group(1)
            if realm in cluster_codes:
                realm = Cluster_codes[realm]
                PullClusterCSV(key)
                print(f'Processing {key} for {realm.upper()}')
                try:
                    CSVprocessor(domain="prod", realm=realm, batch_csv=key, platformOverride="")
                except Exception as e:
                    deployment_batch.append(f'{key} deployment in {realm.upper()} failed to authenticate')
                    print(f"An error occurred while processing {key}: {str(e)}")
                    continue


DEPLOYMENT_OPERATION = 'ONBOARD'
REQUIRED_CSV_FIELDS = ['Building', 'IP Address', 'Camera Name', 'Network Fabric', 'Post Deployment Status']
OPTIONAL_FIELDS = ['Platform']
VALID_PLATFORMS = ['', 'CVR', 'EMBEDDED']


def CSVprocessor(domain, realm, batch_csv, platformOverride=""):
    batch_cameras = read_batch_csv(batch_csv)
    service_client = algalon.get_client(domain, realm)
    building_map = get_building_map(service_client)
    if platformOverride.upper() in VALID_PLATFORMS:
        platform_override = platformOverride.upper()
    else:
        raise Exception(f'Invalid platform override. Valid platformOverride values are: {VALID_PLATFORMS}')

    deployment_group_id = str(uuid.uuid4())
    global cameras_deployed
    df = pd.read_csv(batch_csv)
    for building_code in df['Building'].str.slice(stop=6).unique(): # type: ignore
        deployment_batch.append(f'{building_code} in {realm.upper()} deployment group {deployment_group_id} with {len(batch_cameras)} cameras from {batch_csv}')
    cameras_deployed += len(batch_cameras)
    print(f'Creating deployment group {deployment_group_id} with {len(batch_cameras)} cameras from {batch_csv}')
    for camera in batch_cameras:
        building_arn = building_map[camera['Building']]
        ip_address = camera['IP Address']
        if platform_override != '':
            platform = platform_override
        elif 'Platform' in camera:
            platform = camera['Platform']
        else:
            platform = None
        algalon.create_camera_deployment_task(service_client, deployment_group_id, DEPLOYMENT_OPERATION, building_arn, ip_address, camera['Camera Name'], camera['Network Fabric'], camera['Post Deployment Status'], platform)

def read_batch_csv(filename):
    with open(filename) as csv_file:
        camera_reader = csv.DictReader(csv_file)
        return [camera for camera in camera_reader if validate_camera(camera)]

def get_building_map(service_client):
    return {building.building_name: building.building_id for building in algalon.list_all_buildings(service_client)}

def validate_camera(camera):
    for f in REQUIRED_CSV_FIELDS:
        if f not in camera or not camera[f]:
            raise Exception(f'Camera {camera} is missing required field {f}')
    return True   

def folder_cleanup():
    if os.path.isdir("."):
        for filename in os.listdir("."):
            if filename.endswith(".csv"):
                os.remove(os.path.join(".", filename))
    else:
        path = os.path.join(os.getcwd(), "scripts", "Failed_camData")
        if os.path.isdir(path):
            os.chdir(path)
            for filename in os.listdir("."):
                if filename.endswith(".csv"):
                    os.remove(os.path.join(".", filename))
        else:
            print("Directory 'Failed_camData' not found")
            return
    print('Folder cleaned up')


def deploy_batch():
    # set constants make main() function
    global deployment_batch
    global cameras_deployed
    process_s3_folder(bucket, Cluster_codes)
    print("\n\n")
    for process in deployment_batch:
        print(process)
    print(f"All Cluster complete\nA total of {cameras_deployed} cameras have been deployed")
    folder_cleanup()

if __name__ == "__main__":
    deploy_batch()


#FailedDeploymentsDashUpdate.py

from query_failed_deployments import process
import datetime
import os
import re
import isengard




def PushDashbucket():
    client = isengard.Client()
    session = client.get_boto3_session("BUKET", "OpticsMetricsDashboard")
    s3 = session.client('s3')
    s3.upload_file(
        'all_failed_deployments.csv',
        'camera-deployment-failures',
        'all_failed_deployments.csv'
        )
    return print('File uploaded to S3 bucket')

def current_date():
    return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def past30days():
    return (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

# Set parameters
start_date = past30days()
end_date = current_date()
algalon_servers = [
    "arn",
    "bah",
    "bom",
    "cdg",
    "cmh",
    "cpt",
    "dub",
    "fra",
    "gru",
    "hkg",
    "iad",
    "icn",
    "lhr",
    "mxp",
    "nrt",
    "pdx",
    "sfo",
    "sin",
    "syd",
    "yul",
]

#algalon_servers = ['dub'] # For testing
include_dsn = True

def get_allcsv():
        pattern = r'^all_failed_deployments_.+\.csv$'
        new_filename = 'all_failed_deployments.csv'
        for filename in os.listdir('.'):
            if re.match(pattern, filename):
                root, suffix = os.path.splitext(filename)
                new_filename = 'all_failed_deployments.csv'
                os.rename(filename, new_filename)
                print(f'Renamed {filename} to {new_filename}.')
        return new_filename

def folder_cleanup():
        for filename in os.listdir('.'):
            filepath = os.path.join(filename)
            os.remove(filepath)
        print('Folder cleaned up')

def Dash_DataPull():
    os.makedirs('scripts/Failed_camData', exist_ok=True)
    os.chdir('scripts/Failed_camData')
    process(start_date, end_date, algalon_servers, include_dsn)
    get_allcsv() # Rename file to all_failed_deployments.csv
    PushDashbucket() # Push data to S3 bucket
    folder_cleanup() # Cleanup folder for next run
    return print('Dashboard data pulled and pushed to S3 bucket complete')


if __name__ == '__main__':
    Dash_DataPull()



# Write documentation on how these 3 scripts work together to update the Optics Metrics Dashboard and failed deployments dashboard for 
# operational metrics and informing the customers of the status of their deployments.
# The scripts are written in Python and are run on a daily basis to update the dashboards.
# These scripts also help automating Lenel v Optics parity checking which cameras in Lenel are not in Optics and attempting to onboard them.