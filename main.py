from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize SQS client with environment variables
sqs_client = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

queue_url = "https://sqs.us-east-1.amazonaws.com/174377208419/MyQueue"


class MessageModel(BaseModel):
    action: str
    data: dict


@app.post("/send-message/")
async def send_message(message: MessageModel):
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url, MessageBody=json.dumps(message.dict())
        )
        return {"MessageId": response["MessageId"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
