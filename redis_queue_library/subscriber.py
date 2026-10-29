import json
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
            # skip subscribe/unsubscribe confirmations, only handle published messages
            if isinstance(message, dict) and message.get('type') == 'message':
                try:
                    message_data = message.get('data')
                    if message_data is not None:
                        message_data = json.loads(message_data)
                        # reconstruct data to Message object
                        return handler(Message(channel_name=message.get('channel'), data=message_data.get('data')))
                except Exception as e:
                    logger.error(f"Error during handling message: message: {message} Error: {e}")
                    return Message(channel_name=message.get('channel'), data={"result": "error", "message": f"{e}"})

    def close(self):
        self.sub.close()
        self.conn.close()
