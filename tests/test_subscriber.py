import json

from redis_queue_library.subscriber import Subscriber


def make_subscriber(mocker, messages):
    connection = mocker.patch('redis_queue_library.subscriber.Connection').return_value
    connection.conn.pubsub.return_value.listen.return_value = iter(messages)
    return Subscriber(channel_name='test_channel')


def test_skips_confirmations_and_handles_first_message(mocker):
    payload = json.dumps({'channel_name': 'test_channel', 'data': {'text': 'hi'}})
    subscriber = make_subscriber(mocker, [
        {'type': 'subscribe', 'channel': 'test_channel', 'data': 1},
        {'type': 'message', 'channel': 'test_channel', 'data': payload},
    ])
    handler = mocker.Mock(return_value='handled')

    assert subscriber.listen(handler) == 'handled'
    message = handler.call_args.args[0]
    assert message.get_channel() == 'test_channel'
    assert message.get_data() == {'text': 'hi'}


def test_unsubscribe_confirmation_is_not_an_error(mocker):
    subscriber = make_subscriber(mocker, [{'type': 'unsubscribe', 'channel': 'test_channel', 'data': 0}])
    handler = mocker.Mock()

    assert subscriber.listen(handler) is None
    handler.assert_not_called()


def test_invalid_payload_returns_error_message(mocker):
    subscriber = make_subscriber(mocker, [{'type': 'message', 'channel': 'test_channel', 'data': 'not json'}])

    result = subscriber.listen(mocker.Mock())

    assert result.get_data()['result'] == 'error'
