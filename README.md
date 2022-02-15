# Basic Message Chat
This is a basic implementation of a distributed message chat server, rather than a point to point version.

## How to run (for the current build)
* Make sure to have the Pika, FastAPI, and RabbitMQ on your system
    * ```pip install fastapi[all]```
    * ```pip install pika```
    * [RabbitMQ Installation Guide](https://www.rabbitmq.com/download.html)
* ```python -m uvicorn mess_chat:app --reload```
* Now the cloud server should be running

Name: Kevin Dang

## Libraries Used
* [Python Pika](https://pypi.org/project/pika/#:~:text=Pika%20is%20a%20RabbitMQ%20%28AMQP%200-9-1%29%20client%20library,RabbitMQ%E2%80%99s%20extensions.%20Python%202.7%20and%203.4%2B%20are%20supported.)
* [Python Pydantic](https://pydantic-docs.helpmanual.io/)

## Microservices / API's
* [RabbitM Q](https://www.rabbitmq.com/#features)
* [FastAPI](https://fastapi.tiangolo.com/)

## Useful Information
* [RabbitM Q Introduction](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
* [Pika Documentation](https://pika.readthedocs.io/en/stable/)

## Tutorial Videos
* [Sample FastAPI Post](https://www.youtube.com/watch?v=wS9LfFtXdBs&ab_channel=codeme)
* [RabbitMQ Basics](https://www.youtube.com/watch?v=Cie5v59mrTg&ab_channel=HusseinNasser)