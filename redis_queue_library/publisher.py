import json

from .connection import Connection
from .message import Message


class Publisher:
    def __init__(self):
        self.conn = Connection().conn

    def publish(self, channel_name: str, message: dict):
        self.conn.publish(channel=channel_name, message=json.dumps(Message(channel_name, message).to_json()))
