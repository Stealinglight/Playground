#!/bin/bash

if [ "$#" -ne 3 ] ; then
  echo "Usage: $0 <account> <region> <profile>"
  exit 1
fi

accountId=$1
region=$2
profile=$3
json=$(curl -k --location-trusted -c ~/.midway/cookie -b ~/.midway/cookie -X POST -H "Accept: application/json" -d "{\"awsAccountId\":\"$1\", \"awsPartition\": \"aws\"}" https://iibs-midway.corp.amazon.com/GetSecurityTokenByAccount)

export AWS_ACCESS_KEY_ID=$(echo $json | jq -r ".accessKeyId")
export AWS_SECRET_ACCESS_KEY=$(echo $json | jq -r ".secretAccessKey")
export AWS_SESSION_TOKEN=$(echo $json | jq -r ".sessionToken")

# aws configure set aws_access_key_id `echo $AWS_ACCESS_KEY_ID`
# aws configure set aws_secret_access_key `echo $AWS_SECRET_ACCESS_KEY`
# aws configure set aws_session_token `echo $AWS_SESSION_TOKEN`
# aws configure set default.region `echo $region`

aws configure --profile $profile
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
echo $AWS_SESSION_TOKEN
echo $region