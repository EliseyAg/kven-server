from producer import Producer
from consumer import Consumer


class RabbitMQManager:
    def __init__(self, host, port):
        self.producer = Producer(host, port)
        self.consumer = Consumer(host, port)

    def declare_queue(self, name, durable=True):
        self.ch.queue_declare(queue=name, durable=durable)
