import pytest

from redis_queue_library.connection import Connection


@pytest.fixture
def redis_mock(mocker, monkeypatch):
    for name in ('REDIS_USERNAME', 'REDIS_PASSWORD', 'REDIS_SSL', 'REDIS_SSL_CA_CERT'):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv('REDIS_HOST', 'redis.example')
    monkeypatch.setenv('REDIS_PORT', '6380')
    return mocker.patch('redis_queue_library.connection.redis.Redis')


def test_plain_connection(redis_mock):
    connection = Connection(_env_file=None)

    kwargs = redis_mock.call_args.kwargs
    assert kwargs['host'] == 'redis.example'
    assert kwargs['port'] == 6380
    assert kwargs['protocol'] == 2
    assert 'ssl' not in kwargs
    assert connection.conn is redis_mock.return_value


def test_ssl_with_ca_cert(redis_mock, monkeypatch):
    monkeypatch.setenv('REDIS_SSL', 'true')
    monkeypatch.setenv('REDIS_SSL_CA_CERT', '/certs/ca.pem')

    Connection(_env_file=None)

    kwargs = redis_mock.call_args.kwargs
    assert kwargs['ssl'] is True
    assert kwargs['ssl_ca_certs'] == '/certs/ca.pem'


def test_ssl_without_ca_cert_still_uses_tls(redis_mock, monkeypatch):
    monkeypatch.setenv('REDIS_SSL', 'true')

    Connection(_env_file=None)

    kwargs = redis_mock.call_args.kwargs
    assert kwargs['ssl'] is True
    assert kwargs['ssl_ca_certs'] is None


def test_empty_optional_variables_use_defaults(redis_mock, monkeypatch):
    for name in ('REDIS_USERNAME', 'REDIS_PASSWORD', 'REDIS_SSL', 'REDIS_SSL_CA_CERT'):
        monkeypatch.setenv(name, '')

    connection = Connection(_env_file=None)

    assert connection.redis_ssl is False
    assert connection.redis_password is None
    assert 'ssl' not in redis_mock.call_args.kwargs


def test_conn_is_not_read_from_environment(redis_mock, monkeypatch):
    monkeypatch.setenv('CONN', 'not-a-client')

    connection = Connection(_env_file=None)

    assert connection.conn is redis_mock.return_value
