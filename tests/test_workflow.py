import threading
import time
import unittest

from dotenv import load_dotenv

from redis_queue_library.message import Message
from redis_queue_library.publisher import Publisher
from redis_queue_library.subscriber import Subscriber


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.received_messages = []
        self.subscriber = Subscriber(channel_name='test_channel')

    def message_handler(self, message):
        self.received_messages.append(message)

    def start_subscriber(self):
        self.subscriber.listen(handler=self.message_handler)

    def test_message_received(self):
        message = Message(channel_name='test_channel', data={'text': 'Hello, World!'})
        # start subscriber in a separate thread, so it does not block the main thread
        subscriber_thread = threading.Thread(target=self.start_subscriber)
        subscriber_thread.start()

        publisher = Publisher()
        publisher.publish(channel_name=message.get_channel(), message=message.get_data())
        # wait for the message to be processed
        time.sleep(1)

        # close the subscriber
        self.subscriber.close()
        subscriber_thread.join()

        self.assertEqual(len(self.received_messages), 1)
        self.assertEqual(self.received_messages[0].get_channel(), "test_channel")
        self.assertEqual(self.received_messages[0].get_data(), message.get_data())

