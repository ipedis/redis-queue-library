from typing import Any

import redis
from pydantic import BaseSettings


class Connection(BaseSettings):
    redis_host: str
    redis_username: str | None
    redis_password: str | None
    redis_port: int
    conn: Any

    class Config:
        env_file = '.env'

    def __init__(self, **values: Any):
        super().__init__(**values)
        self.conn = redis.StrictRedis(host=self.redis_host, port=self.redis_port, charset="utf-8",
                                      decode_responses=True, username=self.redis_username, password=self.redis_password)

    def get_connection(self):
        if self.conn is None:
            self.conn = redis.StrictRedis(host=self.redis_host, port=self.redis_port, charset="utf-8",
                                          decode_responses=True, username=self.redis_username,
                                          password=self.redis_password)

        return self.conn
