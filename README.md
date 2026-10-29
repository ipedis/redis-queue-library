# redis-queue-library

A minimal Redis pub/sub wrapper: a `Publisher` that sends JSON messages on a channel and a `Subscriber` that receives them, configured from environment variables.

## Installation

Requires Python >= 3.12 and redis-py >= 5.2. Add it as a git dependency of your project:

```bash
# uv
uv add "redis-queue-library @ git+https://github.com/ipedis/redis-queue-library.git@v2.0.0"
```

```toml
# Poetry
redis-queue-library = {git = "https://github.com/ipedis/redis-queue-library.git", rev = "v2.0.0"}
```

## Configuration

Configuration is read from environment variables, or from a `.env` file in the current working directory. Empty values are treated as unset.

| Variable | Required | Default | Description |
|---|---|---|---|
| `REDIS_HOST` | yes | | Redis host |
| `REDIS_PORT` | yes | | Redis port |
| `REDIS_USERNAME` | no | none | ACL user (`default` for a plain `requirepass`) |
| `REDIS_PASSWORD` | no | none | Password |
| `REDIS_SSL` | no | `false` | Connect over TLS. The server certificate is always verified |
| `REDIS_SSL_CA_CERT` | no | system CA store | Path to the CA bundle used to verify the server when `REDIS_SSL=true` |

## Usage

```python
from redis_queue_library.publisher import Publisher
from redis_queue_library.subscriber import Subscriber

subscriber = Subscriber(channel_name="jobs")      # subscribes immediately

Publisher().publish(channel_name="jobs", message={"job_id": 42, "status": "done"})

def handle(message):
    print(message.get_channel(), message.get_data())   # jobs {'job_id': 42, 'status': 'done'}

subscriber.listen(handler=handle)
subscriber.close()
```

Behaviour to know about:

- `listen(handler)` blocks until **one** message is received, calls `handler(Message)` and returns the handler's return value. Call it in a loop (usually in a thread) to keep consuming.
- If the payload cannot be decoded or the handler raises, the error is logged on the `listener` logger and `listen` returns a `Message` whose data is `{"result": "error", "message": "<error>"}` instead of raising.
- Messages are standard Redis pub/sub: subscribers that are not connected when a message is published never receive it.
- On the wire, the payload is the JSON envelope `{"channel_name": "<channel>", "data": <message dict>}`.
- The client always uses the RESP2 protocol, so the behaviour is identical on every supported redis-py version.

## Development

The project is managed with [uv](https://docs.astral.sh/uv/).

```bash
uv sync                  # create .venv and install all dependencies
uv run pytest            # run the tests
uv run pip-audit         # check dependencies for known vulnerabilities
```

`tests/test_workflow.py` publishes and receives a real message: it runs against the Redis set by `REDIS_HOST`/`REDIS_PORT`/`REDIS_USERNAME`/`REDIS_PASSWORD` (defaults `localhost:6379`, optionally from a gitignored `tests/.env`) and is skipped when that server is not reachable. For example:

```bash
docker run -d --rm -p 127.0.0.1:6379:6379 redis:8.2-alpine
uv run pytest
```

### Demo

`docker compose up --build` starts a Redis server and runs `demo/demo_script.py`, which prints:

```
Received message from test_channel: {'data': 'Hello World!'}
```

## Migrating from v1 to v2

- Python >= 3.12 is required: set `requires-python = ">=3.12"` (uv) or `python = ">=3.12,..."` (Poetry) in the consuming project.
- `REDIS_SSL=true` now always connects over TLS, verifying the server certificate against `REDIS_SSL_CA_CERT` or, when it is not set, the system CA store. In v1, `REDIS_SSL=true` without `REDIS_SSL_CA_CERT` silently used a plain-text connection.
- `REDIS_USERNAME`, `REDIS_PASSWORD` and `REDIS_SSL_CA_CERT` are optional, and empty values (`REDIS_SSL=`) fall back to the defaults instead of failing validation.
- The client is created with `protocol=2`. redis-py 8 switched the default to RESP3; v1 always used RESP2 because it required redis-py 5.
- `Subscriber.listen` ignores subscribe/unsubscribe confirmations. In v1, an unsubscribe confirmation was returned as an error `Message`.
- `Connection.conn` is now a read-only property backed by a private attribute; it is no longer a settings field (it could be overridden by a `CONN` environment variable).
- The library no longer installs `pytest` or `pytest-mock`. If a project used them through this library, it must declare them itself.

## License

Apache License 2.0, see [LICENSE](LICENSE).
