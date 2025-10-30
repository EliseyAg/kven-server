from pika import BlockingConnection


class Consumer:
    def __init__(self, ch):
        self.ch = ch

    def add_consume(self, queue, callback):
        self.ch.basic_consume(
            queue=queue,
            on_message_callback=callback,
        )

    def start_consuming(self):
        self.ch.start_consuming()
