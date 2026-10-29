# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

If a `../CLAUDE.md` exists (workspace checkout), read it first: it holds the rules shared with the services that depend on this library.

## What this is

A small public Python library (Apache-2.0) wrapping Redis pub/sub: `Publisher` sends JSON messages, `Subscriber` receives them. Several services depend on it by git tag, so the public API, the wire format and the `REDIS_*` variables are a contract: a change to any of them is a breaking change (major version) and must be validated first.

## Commands

uv project (`uv.lock`), build backend hatchling, Python >= 3.12 (`.python-version`).

```bash
uv sync
uv run pytest                                            # all tests
uv run pytest tests/test_connection.py                   # one file
uv run pytest tests/test_workflow.py::TestWorkflow::test_message_received   # one test
uv run --with redis==5.2.1 pytest                        # lowest supported redis-py
uv run pip-audit
uv build
docker compose up --build                                # demo: redis + demo/demo_script.py
```

`tests/test_workflow.py` (marker `integration`) needs a Redis from `REDIS_HOST`/`REDIS_PORT`/`REDIS_USERNAME`/`REDIS_PASSWORD` (default `localhost:6379`, optional gitignored `tests/.env`, see `tests/conftest.py`) and is skipped when unreachable, so a green run without Redis does not cover pub/sub. The other tests mock `redis.Redis` / `Connection`. No linter or formatter is configured.

## Architecture

- `connection.py`: `Connection` is a `pydantic-settings` `BaseSettings` reading `REDIS_*` from the environment or from `.env` **in the current working directory** (`env_ignore_empty=True`). It builds the `redis.Redis` client in its constructor, exposed as the `conn` property. `REDIS_SSL=true` always means TLS with certificate verification (CA from `REDIS_SSL_CA_CERT` or system store). `protocol=2` is forced because redis-py 8 defaults to RESP3; keep it.
- `message.py`: `Message(channel_name, data: dict)`.
- `publisher.py`: `Publisher()` opens its own connection; `publish(channel, dict)` sends `json.dumps({"channel_name": ..., "data": <dict>})`.
- `subscriber.py`: `Subscriber(channel)` subscribes at construction. `listen(handler)` is **one-shot**: it ignores non-`message` events, calls the handler for the first published message and **returns** its result; on error it logs and returns an error `Message` instead of raising. Callers loop themselves; turning it into a blocking loop is a breaking change.

The code must work on every redis-py version allowed by `pyproject.toml` (consumers resolve redis together with other libraries such as Celery/kombu): do not use constructor arguments that only exist in recent redis-py.

## Public repository hygiene

No `.env` file is tracked; the demo gets its config from `docker-compose.yml` (demo-only password on a non-exposed Redis). Never commit real hosts, credentials, internal URLs or details of the infrastructure that uses this library. The sdist only ships `redis_queue_library`, `tests`, `README.md` and `LICENSE`.
