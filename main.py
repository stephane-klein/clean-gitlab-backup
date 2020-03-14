#!/usr/bin/env python3
import os
import sys
import logging
import time

import boto3
import schedule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logging.getLogger('schedule').propagate = False

variable_env_required = [
    'NUMBER_BACKUP_TO_KEEP',
    'S3_REGION_NAME',
    'S3_ENDPOINT_URL',
    'S3_AWS_ACCESS_KEY_ID',
    'S3_AWS_SECRET_ACCESS_KEY',
    'S3_BUCKET_NAME',
    'START_EVERY_DAY_AT_UTC'
]

variable_env_required_missing = False
for v in variable_env_required:
    if v not in os.environ.keys():
        logging.error('%s variable env missing', v)
        variable_env_required_missing = True

if variable_env_required_missing:
    sys.exit(1)

if not os.getenv('NUMBER_BACKUP_TO_KEEP').isnumeric():
    logging.error(
        'NUMBER_BACKUP_TO_KEEP variable env value ("%s") must be numeric',
        os.getenv('NUMBER_BACKUP_TO_KEEP')
    )

def job():
    logging.info('Start GitLab old backup cleaning...')

    s3 = boto3.client(
        's3',
        region_name=os.getenv('S3_REGION_NAME'),
        endpoint_url=os.getenv('S3_ENDPOINT_URL'),
        aws_access_key_id=os.getenv('S3_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('S3_AWS_SECRET_ACCESS_KEY')
    )

    bucket_name = os.getenv('S3_BUCKET_NAME')

    resp = s3.list_objects_v2(Bucket=bucket_name)
    for key in sorted(
            [row['Key'] for row in resp['Contents']]
        )[:-int(os.getenv('NUMBER_BACKUP_TO_KEEP'))]:
        logging.info('Delete %s file', key)
        s3.delete_object(
        Bucket=bucket_name,
        Key=key
        )

    logging.info('GitLab old backup clean done')

schedule.every().day.at(os.getenv('START_EVERY_DAY_AT_UTC')).do(job)
logging.info(
    'clean-gitlab-backup started: Running job Every 1 day at %s UTC',
    os.getenv('START_EVERY_DAY_AT_UTC')
)

while True:
    schedule.run_pending()
    time.sleep(1)