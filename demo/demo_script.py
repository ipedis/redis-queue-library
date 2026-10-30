from redis_queue_library.publisher import Publisher
from redis_queue_library.subscriber import Subscriber


def main():
    subscriber = Subscriber(channel_name="test_channel")
    publisher = Publisher()
    publisher.publish(channel_name="test_channel", message={"data": "Hello World!"})
    subscriber.listen(handler=message_handler)


def message_handler(message):
    print(f"Received message from {message.get_channel()}: {message.get_data()}")


if __name__ == "__main__":
    main()
