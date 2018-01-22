#!/usr/local/bin/python2

import argparse
import sys
import boto3
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_REGION = ''
INSTANCE_TYPE = ''

parser = argparse.ArgumentParser(description='Take AWS keys, region, and instance type.')

parser.add_argument('--AWS_ACCESS_KEY_ID', action="store", help='AWS access key')
parser.add_argument('--AWS_SECRET_ACCESS_KEY', action="store", help='AWS secret key')
parser.add_argument('--AWS_REGION', action="store", help='AWS region e.g. us-east-1')
parser.add_argument('--INSTANCE_TYPE', action="store", help='AWS instance type, e.g. t2.micro')

inputs = parser.parse_args()

# boto3 client for ec2 API
client = boto3.client('ec2',
                        aws_access_key_id=inputs.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=inputs.AWS_SECRET_ACCESS_KEY,
                        region_name=inputs.AWS_REGION)

# find the Amazon Linux AMI for this region; overdescribe the filter
images = client.describe_images(Filters=[
                            {'Name': 'name', 'Values': ['amazon*']}, 
                            {'Name': 'architecture', 'Values': ['x86_64']},
                            {'Name': 'virtualization-type', 'Values': ['hvm']},
                            {'Name': 'root-device-type', 'Values': ['ebs']},
                            {'Name': 'owner-id', 'Values': ['331665368908']}])

ami = images['Images'][0]['ImageId']

# launch an instance
response = client.run_instances(
            ImageId=ami,
            InstanceType=inputs.INSTANCE_TYPE,
            MaxCount=1, MinCount=1)

# parse response, get instance ID
instance = response['Instances'][0]['InstanceId']

# poll EC2 API until instance 'come(s) online'
while True:
    state = client.describe_instances(Filters=[{'Name': 'instance-id', 'Values': [instance]}])
    status = state['Reservations'][0]['Instances'][0]['State']['Name']
    if status == 'running':
        break

launch = state['Reservations'][0]['Instances'][0]['LaunchTime']

# print instance launch time to STDOUT
print "Launch time: %s" % launch
