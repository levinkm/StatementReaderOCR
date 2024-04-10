import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import statements
from src.api.utils.rabbitmq import PikaClient
from src.api.config.settings import DEBUG,ORIGINS
import logging

logger = logging.getLogger(__name__)


# to create all the tables using the already defined schema
# models.Base.metadata.create_all(bind=Engine)

# class PikaClient:
#     def __init__(self, process_callable):
#         self.process_callable = process_callable
#         self.publish_queue_name = 'bank-statements'
#         self.connection = None
#         self.channel = None
#         self.publish_queue = None
#         self.callback_queue = None
#         logger.info('Pika connection initialized')

#     async def consume(self, loop):
#         """Setup message listener with the current running loop"""
#         self.connection = await aio_pika.connect_robust(host=config('RABBIT_HOST', default='127.0.0.1'), port=5672, loop=loop) # type: ignore
#         self.channel = await self.connection.channel()
#         queue = await self.channel.declare_queue('bank-statements')
#         await queue.consume(self.process_incoming_message, no_ack=False) # type: ignore
#         logger.info('Established pika async listener')
#         return self.connection

#     async def process_incoming_message(self, message: aio_pika.IncomingMessage):
#         async with message.process():
#             logger.info('Received message')
#             print(f"Received message: {message.body}")
#             print(f"Message properties: {message.properties}")
#             print(f"Message headers: {message.headers}")
#             print(f"Message delivery tag: {message.delivery_tag}")
#             print(f"Message redelivered: {message.redelivered}")
#             print(f"Message exchange: {message.exchange}")
#             print(f"Message routing key: {message.routing_key}")    
#             print(f"Message content type: {message.content_type}")


class App(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    def log_incoming_message(cls, message: dict):
        """Method to do something meaningful with the incoming message"""
        logger.info('Here we got incoming message %s', message)
    
    
    




app = App(debug=DEBUG, title="Fedhatrac OCR API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define startup event handler


# Include your router
app.include_router(statements.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task

