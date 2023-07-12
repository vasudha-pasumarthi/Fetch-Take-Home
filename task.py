import subprocess
import json
import time
# import boto3
import psycopg2
from datetime import datetime
from hashlib import sha256

# SQS queue url
queue_url = 'http://localhost:4566/000000000000/login-queue'

# function to mask PII data


def mask_pii(data):
    try:
        # Hash device_id and ip using sha256
        data['masked_device_id'] = sha256(
            data['device_id'].encode()).hexdigest()
        data['masked_ip'] = sha256(data['ip'].encode()).hexdigest()
        return data
    except Exception as e:
        print(e)


# Connect to Postgres DB
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="postgres",
)

# function to get current timestamp


def current_date():
    return str(datetime.now().strftime('%Y-%m-%d'))

# function to insert data into user_logins table


def write_to_db(data):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                    (data['user_id'], data['device_type'], data['masked_ip'], data['masked_device_id'], data['locale'], data['app_version'], current_date()))
        conn.commit()
    except Exception as e:
        print(e)


while True:
    try:

        # Receive message from SQS queue
        response = subprocess.run(['awslocal', 'sqs', 'receive-message', '--queue-url',
                                   queue_url], capture_output=True)
        if response.returncode == 0:
            # Extract the message body
            message_body = json.loads(response.stdout)
        # Extract the user_id field
            receipt_handle = message_body['Messages'][0]['ReceiptHandle']

            data = json.loads(message_body['Messages'][0]['Body'])
            # print(data)

            subprocess.run(['awslocal', 'sqs', 'delete-message', '--queue-url',
                            queue_url, '--receipt-handle', receipt_handle], capture_output=True)

            # IF there is invalid / unwanted message in Queue to ignore and remove it
            if data.get('user_id') == None:
                continue

            data = mask_pii(data)
            data["app_version"] = str(data["app_version"])
            write_to_db(data)
            # print(data)
            # print("Process End")

        else:
            print(response.stderr)
        # time.sleep(5)
    except Exception as e:
        print(e)
        print("Process ended")
        break
