import pika
from pika.adapters.asyncio_connection import AsyncioConnection

import json
import io
import asyncio

from fastapi import BackgroundTasks
import pika.adapters.asyncio_connection
from process_statements import process_file
import base64

background_tasks = BackgroundTasks()

def publish_bank_statement_to_rabbitmq(bank_statement_data: dict, queue_name: str, host: str = 'localhost', port: int = 5672):

    message = json.dumps(bank_statement_data)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='', routing_key=queue_name, body=message)

    connection.close()
pika.adapters.asyncio_connection.AsyncioConnection.channel

def send_notification(message):
    # Placeholder function to send notification (e.g., email, push notification, etc.)
    print("Notification:", message)





async def consume_from_rabbitmq(queue_name: str, host: str = 'localhost', port: int = 5672):
    # Establish connection to RabbitMQ server using asyncio adapter
    connection =  AsyncioConnection(pika.ConnectionParameters(host=host, port=port))
    channel =  connection.channel()
    # Declare the queue if it doesn't exist
    channel.queue_declare(queue=queue_name)

    # Callback function to process received messages
    def callback(ch, method, properties, body):
        # Process the received message
        bank_statement_data = json.loads(body)
        file = bank_statement_data.get('file')
        password = bank_statement_data.get('password')
        if file:
            background_tasks.add_task(process_file,file=file,password=password)
        else:
            raise ValueError("File not found in bank statement data")

    # Set up a consumer to consume messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Start consuming messages
    print("Waiting for messages. To exit press CTRL+C")

