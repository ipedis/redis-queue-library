import unittest

from redis_queue_library.message import Message


class TestMessage(unittest.TestCase):
    def test_message(self):
        message = Message(channel_name='test', data={'text': 'Hello, World!'})
        self.assertEqual(message.get_channel(), "test")
        self.assertEqual(message.get_data(), {'text': 'Hello, World!'})
        self.assertEqual(message.to_json(), {"channel_name": "test", "data": {"text": "Hello, World!"}})

