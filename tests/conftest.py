import os

import pytest
import redis
from dotenv import load_dotenv

# Optional local overrides (tests/.env is gitignored), then defaults for a local Redis.
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
os.environ.setdefault('REDIS_HOST', 'localhost')
os.environ.setdefault('REDIS_PORT', '6379')


@pytest.fixture(scope='session')
def redis_available():
    client = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']),
                         username=os.environ.get('REDIS_USERNAME') or None,
                         password=os.environ.get('REDIS_PASSWORD') or None, protocol=2)
    try:
        client.ping()
    except redis.exceptions.RedisError as e:
        pytest.skip(f"Redis not reachable at {os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}: {e}")
    finally:
        client.close()
