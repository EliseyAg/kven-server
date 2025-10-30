from pika import ConnectionParameters, BlockingConnection


class Producer:
    def __init__(self, host, port):
        self.connection_parameters = ConnectionParameters(
            host=host,
            port=port,
        )

        self.conn = BlockingConnection(self.connection_parameters)
        self.ch = self.conn.channel()

    def publish(self, routing_key, body, exchange=""):
        self.ch.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
        )
