from pika import ConnectionParameters, BlockingConnection


class Consumer:
    def __init__(self, host, port):
        self.connection_parameters = ConnectionParameters(
            host=host,
            port=port,
        )

        self.conn = BlockingConnection(self.connection_parameters)
        self.ch = self.conn.channel()

    def add_consume(self, queue, callback):
        self.ch.basic_consume(
            queue=queue,
            on_message_callback=callback,
        )

    def start_consuming(self):
        self.ch.start_consuming()
