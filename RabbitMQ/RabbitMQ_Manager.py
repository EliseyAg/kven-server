from RabbitMQ.producer import Producer
from RabbitMQ.consumer import Consumer

from pika import ConnectionParameters, BlockingConnection


class RabbitMQManager:
    connection_parameters = None
    conn = None
    ch = None

    producers = []
    consumers = []

    @staticmethod
    def __init__(host, port):
        RabbitMQManager.connection_parameters = ConnectionParameters(
            host=host,
            port=port,
        )

        RabbitMQManager.conn = BlockingConnection(RabbitMQManager.connection_parameters)
        RabbitMQManager.ch = RabbitMQManager.conn.channel()

    @staticmethod
    def add_producer():
        producer = Producer(RabbitMQManager.ch)
        RabbitMQManager.producers.append(producer)
        return len(RabbitMQManager.producers)

    @staticmethod
    def publish(producer_id, routing_key, body, exchange=""):
        producer = RabbitMQManager.producers[producer_id]
        producer.publish(routing_key, body, exchange)

    @staticmethod
    def add_consumer():
        consumer = Consumer(RabbitMQManager.ch)
        RabbitMQManager.consumers.append(consumer)
        return len(RabbitMQManager.consumers)

    @staticmethod
    def add_consume(consumer_id, queue, callback):
        consumer = RabbitMQManager.producers[consumer_id]
        consumer.publish(queue, callback)

    @staticmethod
    def start_consuming(consumer_id):
        consumer = RabbitMQManager.producers[consumer_id]
        consumer.start_consuming()

    @staticmethod
    def declare_queue(name, durable=True):
        RabbitMQManager.ch.queue_declare(queue=name, durable=durable)
