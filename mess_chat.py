from fastapi import FastAPI
from pydantic import BaseModel

from rmq import MessageServer

app = FastAPI()

# This class will create an object that will create an message
class Message(BaseModel):
    target_channel: str
    message: str

@app.get("/")
async def startup():
    return 'The API is currently running'
# we want to use this to create and send the message
# we want a Destination and message_content
@app.post("/send/")
async def send(message : Message, target_queue: str):
    list_of_messages = []
    connect = MessageServer()
    connect.send_message(message_content = message.message, target_queue = target_queue)
    list_of_messages.append(message)
    return {
        'message_count' : len(list_of_messages),
        'messages' : list_of_messages
    }

# we need to connect to the queue from here
# we should use max messages
@app.get("/messages/")
async def messages(message_count: int, queue_destination: str):
    connect = MessageServer()
    messages_received = connect.receieve_messages(num_messages = message_count, destination = queue_destination)
    return {
        'message_count' : len(messages_received),
        'data' : messages_received
    }