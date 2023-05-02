class Message:
    def __init__(self, channel_name: str, data: dict):
        self.channel_name: str = channel_name
        self.data: dict = data

    def get_channel(self) -> str:
        return self.channel_name

    def get_data(self) -> dict:
        return self.data

    def to_json(self) -> dict:
        return {
            "channel_name": self.channel_name,
            "data": self.data
        }
