from typing import Any

import redis
from pydantic import PrivateAttr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Connection(BaseSettings):
    # Empty variables (e.g. `REDIS_SSL_CA_CERT=`) fall back to the defaults below.
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore',
                                      env_ignore_empty=True)
    redis_host: str
    redis_port: int
    redis_username: str | None = None
    redis_password: str | None = None
    redis_ssl: bool = False
    redis_ssl_ca_cert: str | None = None
    _conn: redis.Redis | None = PrivateAttr(default=None)

    def __init__(self, **values: Any):
        super().__init__(**values)
        self._conn = self.__redis_client()

    @property
    def conn(self) -> redis.Redis:
        return self.get_connection()

    def get_connection(self) -> redis.Redis:
        if self._conn is None:
            self._conn = self.__redis_client()

        return self._conn

    def __redis_client(self) -> redis.Redis:
        options: dict[str, Any] = {}
        if self.redis_ssl:
            # Certificates are always verified: against REDIS_SSL_CA_CERT when set,
            # otherwise against the system CA store.
            options = {"ssl": True, "ssl_ca_certs": self.redis_ssl_ca_cert}

        # protocol=2: redis-py >= 8 defaults to RESP3, keep RESP2 so every redis-py version behaves the same.
        return redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True,
                           username=self.redis_username, password=self.redis_password, protocol=2, **options)
