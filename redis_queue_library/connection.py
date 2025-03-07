from typing import Any

import redis
from pydantic_settings import BaseSettings, SettingsConfigDict


class Connection(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    redis_host: str
    redis_username: str | None
    redis_password: str | None
    redis_port: int
    redis_ssl: bool = False
    redis_ssl_ca_cert: str | None
    conn: redis.StrictRedis | None = None

    def __init__(self, **values: Any):
        super().__init__(**values)
        self.conn = self.__redis_client()

    def get_connection(self):
        if self.conn is None:
            self.conn = self.__redis_client()

        return self.conn

    def __redis_client(self):
        if self.redis_ssl and self.redis_ssl_ca_cert is not None:
            return redis.StrictRedis(host=self.redis_host, port=self.redis_port, charset="utf-8",
                                     decode_responses=True, username=self.redis_username,
                                     password=self.redis_password, ssl=True, ssl_ca_certs=self.redis_ssl_ca_cert)

        return redis.StrictRedis(host=self.redis_host, port=self.redis_port, charset="utf-8",
                             decode_responses=True, username=self.redis_username,
                             password=self.redis_password)
