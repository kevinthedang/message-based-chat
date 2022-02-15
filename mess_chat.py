from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

list_of_messages = []

class Message(BaseModel):
    name: str
    address: str
    message: str

# we want to use this to create and send the message
@app.post("/send/")
async def send(message : Message):
    list_of_messages.append(message)
    return {
        'message_count' : len(list_of_messages),
        'data' : list_of_messages
    }

# we need to connect to the queue from here
@app.get("/messages/")
async def messages():
    return {
        'message_count' : len(list_of_messages),
        'data' : list_of_messages
    }