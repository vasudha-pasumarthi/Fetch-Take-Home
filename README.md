# Fetch Rewards Task
 Creating ETL processes Data Engineering Role

Exercise Link  -  https://fetch-hiring.s3.amazonaws.com/data-engineer/pii-masking.pdf

## Initial Project Setup

1. Install Docker desktop it has Docker Compose Inbuilt.
```
https://docs.docker.com/get-docker/
```
2.  Install Postgress psql
```
https://www.postgresql.org/download/
```


## To run the code
1. Clone this repo.
```bash
git clone https://github.com/ahirsarthak/fetch-project.git
```

2. Go into the cloned repo.
```bash
cd fetch-project
```

3. Install required dependencies.
For AWS CLI Subprocess Calls
```bash
pip install subprocess.run
```
For Database PSQL Connection
```bash
pip install psycopg2-binary
```
For Hashing
```bash
pip install hashlib
```
AWS-CLI
```bash
pip install awscli-local
```

4. Run this Docker code so that you container is up and running and all the data from localstack is loaded.
```bash
docker-compose up
```
and Once you're done with everything to shut it down CTRL + C or
```
docker-compose down 
```


5. Run Python code in terminal to perform ETL process.
```bash
python task.py
```
and CTRL + C to end the process of ETL

# Solution Development Decesions 
1. How will you read messages from the queue?
   - I initialy tried using boto3 but it was throwing me error that I require AWS Credentials.
  So I searched online the subprocess of python where I wrote response code as a form of AWS-CLI.
example - `awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue`
  
2. How will you mask the PII data so that duplicate values can be identified?
   - I used sha256 funtion of hashlib library to do the following.
   And it also takes care of detecting the duplicate values as it produces same hash if same input is given so if the hash value is same then the value is a duplicate
   
3. What will be your strategy for connecting and writing to Postgres?
   - For connection I used psycopg2.
   It has set of inbuilt python funtions to connect with psql databse '.connect' and write into it '.execute'
   
6. Where and how will your application run? 
   - The application can run locally mentioned above and can be stopped using ctrl+C

# QUESTIONS

1. How would you deploy this application in production?
   - Create AWS SQS Queue
   - Create Postgress Database in AWS or any other service
   - Packaging the application as a Docker Container and Publish it in registry
   - Create a ECS service and then connect it with SQS Queue and Postfres database

2. What other components would you want to add to make this production ready?
   - More Error Handling and testing - I caught few bad values in the localstack
   - Implement a Monitor service such as cloudwatch
   - Create Automated backups
   - Make everything more secured using IAM roles

3. How can this application scale with a growing dataset?
   - Using a loadbalancer to create multiple instance of the application.
   - Create a Cloudwatch log to keep an eye on performace
   - Use of auto scaling groups in case the load is increased on the application.
   - Can also use various Data Warehousing solutions available such as AWS Redshift.

4. How can PII be recovered later on?
   - One way is by using the hashed values of the PII data as a reference, and comparing it to the original data that was hashed.This is done by applying the same hash function to the original data, and comparing the output to the stored hashed value. If the two values match, it is likely that the original data was used to generate the hashed value.
   -  However,is not foolproof, as hash collisions can occur. Therefore, it is also important to store the original data in a secure, encrypted location, in case it is needed for recovery.

5. What are the assumptions you made?
   - SQS queue and PostfreSQL are running on localhost and can be accessed using AWS CLI calls and Postgre server already exists with all the specified table with data columns.
   - Assumed that SQS queue are in the correct sequence and format and it can be accessed as it is using the AWS-CLI
   - Also SQS Message has to be deleted after it is once read and stored in the SQL Database.
   - Had to make one change in SQL data type of "app_version" from given int to a char(9). As the version of applications can be '2.5.0' which is not a float nor an integer and to preserve the standard format the Table data type of app version had to be changed to string.
   - Couldn't use boto3 as it required AWS region and AWS Credentials.
 
  
  
 
