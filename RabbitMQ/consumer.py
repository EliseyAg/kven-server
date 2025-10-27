from pika import ConnectionParameters, BlockingConnection


connection_parameters = ConnectionParameters(
    host="localhost",
    port=5672,
)


def process_message(ch, method, properties, body):
    print(f"Получено сообщение: {body.decode()}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    with BlockingConnection(connection_parameters) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue="messages", durable=True)

            ch.basic_consume(
                queue="messages",
                on_message_callback=process_message,
            )

            print("жду сообщений")
            ch.start_consuming()


if __name__ == "__main__":
    main()
