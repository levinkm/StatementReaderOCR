import pika
from pika.adapters.asyncio_connection import AsyncioConnection


import json
import io
import asyncio
import aio_pika
import logging
from decouple import config
from io import BytesIO
from fastapi import BackgroundTasks
import pika.adapters.asyncio_connection
import pika.exceptions
from src.api.utils.process_statements import process_file as pf
from src.api.schemas.schemas import BankStatementUploadModel
import base64

background_tasks = BackgroundTasks()
logger = logging.getLogger(__name__)

def publish_bank_statement_to_rabbitmq(bank_statement_data: dict, queue_name: str, host: str = 'localhost', port: int = 5672):

    message = json.dumps(bank_statement_data)

    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host,port=port))

    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='', routing_key=queue_name, body=message) # type: ignore

    connection.close()


def send_notification(message):
    # Placeholder function to send notification (e.g., email, push notification, etc.)
    # print("Notification:", message)
    pass

class PikaClient:
    def __init__(self, process_callable):
        self.process_callable = process_callable
        self.publish_queue_name = 'bank-statements'
        self.connection = None
        self.channel = None
        self.publish_queue = None
        self.callback_queue = None
        self.lock = asyncio.Lock()  # Initialize a lock for thread safety
        logger.info('Pika connection initialized')

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        self.connection = await aio_pika.connect_robust(host=config('RABBIT_HOST', default='127.0.0.1'), port=5672, loop=loop)  # type: ignore
        self.channel = await self.connection.channel()
        queue = await self.channel.declare_queue('bank-statements')
        await queue.consume(self.process_incoming_message, no_ack=False)  # type: ignore
        logger.info('Established pika async listener')
        return self.connection

    async def process_incoming_message(self, message: aio_pika.IncomingMessage):
        async with self.lock:  # Acquire the lock before processing
            async with message.process():
                logger.info('Received message')

                try:
                    bank_statement_data = json.loads(message.body)
                    file_content = bank_statement_data.get("file_content")
                    decoded_file_content = base64.b64decode(file_content.encode('utf-8'))
                    

                    if decoded_file_content:
                        logger.info('Processing file')
                        # Implement idempotent processing here (e.g., check for processed file)
                        processed_successfully = await self.process_file(file=decoded_file_content)
                        
                        print(processed_successfully.head())
                        logger.info("File processed successfully")

                        # TODO: Implement notification logic (e.g., send email, push notification, etc.
                        # TODO: Implement saving to database (e.g., save to a database table)
                        
                    else:
                        raise ValueError("File not found in bank statement data")
                except (json.JSONDecodeError, ValueError) as e:
                    logger.error(f"Error : {e}")
                    # await message.reject(requeue=True)  # Requeue for later attempts

    async def process_file(self, file):
     
     
        return await pf(file)  #
    







