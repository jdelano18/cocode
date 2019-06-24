import boto3
s3 = boto3.client('s3',
        aws_access_key_id='',
        aws_secret_access_key= '')
bucket_name = 'so-bricks'

import os
files = []
for filename in os.listdir('.'):
    if filename.endswith(".ipynb"):
        files.append(filename)
    else:
        continue

for filename in files:
    s3.upload_file(filename, bucket_name, filename)
