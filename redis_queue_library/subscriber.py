import logging
from typing import Callable

from .connection import Connection
from .message import Message


logger = logging.getLogger('listener')


class Subscriber:
    def __init__(self, channel_name: str):
        self.conn = Connection().conn
        self.sub = self.conn.pubsub()
        self.sub.subscribe(channel_name)

    def listen(self, handler: Callable):
        for message in self.sub.listen():
            if message is not None and isinstance(message, dict):
                try:
                    message_data = message.get('data')
                    if message_data is not None and isinstance(message_data, Message):
                        handler(message_data)
                except Exception as e:
                    logger.error(f"Error during handling message: message: {message} Error: {e}")
