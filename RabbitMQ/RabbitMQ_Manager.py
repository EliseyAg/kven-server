from RabbitMQ.producer import Producer
from RabbitMQ.consumer import Consumer

from pika import ConnectionParameters, BlockingConnection


class RabbitMQManager:
    connection_parameters = None
    conn = None
    ch = None

    producer = None
    consumer = None

    @staticmethod
    def __init__(host, port):
        RabbitMQManager.connection_parameters = ConnectionParameters(
            host=host,
            port=port,
        )

        RabbitMQManager.conn = BlockingConnection(RabbitMQManager.connection_parameters)
        RabbitMQManager.ch = RabbitMQManager.conn.channel()

        RabbitMQManager.producer = Producer(RabbitMQManager.ch)
        RabbitMQManager.consumer = Consumer(RabbitMQManager.ch)

    @staticmethod
    def publish(routing_key, body, exchange=""):
        RabbitMQManager.producer.publish(routing_key, body, exchange)

    @staticmethod
    def add_consume(queue, callback):
        RabbitMQManager.consumer.add_consume(queue, callback)

    @staticmethod
    def start_consuming():
        RabbitMQManager.consumer.start_consuming()

    @staticmethod
    def declare_queue(name, durable=True):
        RabbitMQManager.ch.queue_declare(queue=name, durable=durable)
