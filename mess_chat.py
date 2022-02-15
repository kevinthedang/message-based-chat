from sqlite3 import connect
from fastapi import FastAPI
from pydantic import BaseModel
import pika
import logging

app = FastAPI()

list_of_messages = []

# This class will create an object that will create an message
class Message(BaseModel):
    target_channel: str
    message: str

# we want to use this to create and send the message
# we want a Destination and message_content
@app.post("/send/")
async def send(self, message : Message):
    list_of_messages.append(message)
    return {
        'message_count' : len(list_of_messages),
        'data' : list_of_messages
    }

# we need to connect to the queue from here
# we should use max messages
@app.get("/messages/")
async def messages():
    return {
        'message_count' : len(list_of_messages),
        'data' : list_of_messages
    }