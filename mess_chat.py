from fastapi import FastAPI
from rmq import MessageServer

app = FastAPI()
connect = MessageServer()

@app.get("/")
async def startup():
    return 'The API is currently running'

# we want to use this to create and send the message
# we want a Destination and message_content
@app.post("/send/")
async def send(message : str, target_queue: str):
    list_of_messages = []
    connect.send_message(message_content = message, target_queue = target_queue)
    list_of_messages.append(message)
    return {
        'message_count' : len(list_of_messages),
        'messages' : list_of_messages
    }

# we need to connect to the queue from here
# we should use max messages
@app.get("/messages/")
async def messages(message_count: int, queue_destination: str):
    messages_received = connect.receieve_messages(num_messages = message_count, take_from_queue = queue_destination)
    return {
        'message_count' : len(messages_received),
        'data' : messages_received
    }