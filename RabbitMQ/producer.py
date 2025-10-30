from pika import BlockingConnection


class Producer:
    def __init__(self, ch):
        self.ch = ch

    def publish(self, routing_key, body, exchange=""):
        self.ch.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
        )
