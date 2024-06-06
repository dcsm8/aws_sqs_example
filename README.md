# FastAPI SQS Integration

This project demonstrates how to use FastAPI to send messages to an AWS SQS queue and how to set up an AWS Lambda function to process those messages.

## Prerequisites

- Python 3.10+
- AWS Account
- AWS CLI configured with the necessary permissions
- FastAPI
- Uvicorn
- boto3
- python-dotenv

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/dcsm8/aws_sqs_example.git
cd aws_sqs_example
```

### 2. Create a virtual environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies

```sh
pip install fastapi uvicorn boto3 python-dotenv
```

### 4. Create a `.env` file

Create a `.env` file in the root directory and add your AWS credentials:

```plaintext
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=us-east-1  # Change to your desired region
```

### 5. Update `main.py`

Update the `queue_url` in `main.py` with your actual SQS queue URL:

```python
queue_url = 'https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/MyQueue'  # Replace with your Queue URL
```

## Running the Application

Start the FastAPI application:

```sh
uvicorn main:app --reload
```

### Testing the API

You can test sending messages to the SQS queue using a tool like Postman

#### Using Postman:

1. Set the request type to POST.
2. Set the URL to `http://127.0.0.1:8000/send-message/`.
3. Set the header `Content-Type` to `application/json`.
4. Set the body to:
    ```json
    {
        "action": "process_data",
        "data": {
            "key1": "value1",
            "key2": "value2"
        }
    }
    ```

## Setting Up the Lambda Function

### 1. Create the Lambda Function

1. Log in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to the Lambda Console.
3. Create a new Lambda function named `ProcessSQSEvent` with Python 3.10 runtime.

### 2. Write the Lambda Function Code

Here is an example Lambda function code:

```python
import json

def lambda_handler(event, context):
    for record in event['Records']:
        body = record['body']
        print(f'Received message: {body}')
        try:
            message = json.loads(body)
            print(f'Parsed message: {message}')
            if 'action' in message:
                if message['action'] == 'process_data':
                    print('Processing data...')
                elif message['action'] == 'send_email':
                    print('Sending email...')
                else:
                    print(f'Unknown action: {message["action"]}')
        except json.JSONDecodeError:
            print('Could not parse message body as JSON')
    return {
        'statusCode': 200,
        'body': json.dumps('Messages processed successfully!')
    }
```

### 3. Configure Lambda to Trigger on SQS Messages

1. Add an SQS trigger to your Lambda function and select your SQS queue.
2. Ensure the Lambda function's execution role has permissions to read from the SQS queue. 

### 4. Test the Setup

Send messages using your FastAPI application and check the Lambda logs in CloudWatch to verify the messages are processed correctly.