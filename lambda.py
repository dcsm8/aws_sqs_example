import json


def lambda_handler(event, context):
    for record in event["Records"]:
        # Extract the message body
        body = record["body"]
        print(f"Received message: {body}")

        # Here you can add your message processing logic
        try:
            message = json.loads(body)
            print(f"Parsed message: {message}")

            # Add your processing logic here
            if "action" in message:
                if message["action"] == "process_data":
                    # Perform some processing
                    print("Processing data...")
                elif message["action"] == "send_email":
                    # Send an email
                    print("Sending email...")
                else:
                    print(f'Unknown action: {message["action"]}')

        except json.JSONDecodeError:
            print("Could not parse message body as JSON")

    return {"statusCode": 200, "body": json.dumps("Messages processed successfully!")}
