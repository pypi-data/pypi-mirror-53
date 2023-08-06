# -*- coding: utf-8 -*-
"""Unit tests for the streaming client"""

import pytest
import six
from src.rev_ai import __version__
from src.rev_ai.models.streaming import MediaConfig
from src.rev_ai.streamingclient import RevAiStreamingClient

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


@pytest.mark.usefixtures('mock_streaming_client', 'mock_generator')
class TestStreamingClient():
    def test_constructor(self):
        example_token = 'token'
        example_config = MediaConfig()
        example_version = 'example_version'
        example_error_func = lambda example_error: example_error
        example_close_func = lambda code, reason: '{}:{}'.format(code, reason)
        example_connect_func = lambda id: id
        example_client = RevAiStreamingClient(
            example_token,
            example_config,
            example_version,
            example_error_func,
            example_close_func,
            example_connect_func
        )

        assert example_client.on_error("Example Error") == 'Example Error'
        assert example_client.on_connected("Example ID") == 'Example ID'
        assert example_client.on_close('1', 'Example Reason') == '1:Example Reason'
        assert example_client.base_url == 'wss://api.rev.ai/speechtotext/example_version/stream'

    def test_constructor_using_defaults(self):
        example_token = 'token'
        example_config = MediaConfig()
        example_client = RevAiStreamingClient(example_token, example_config)

        assert example_client.access_token == 'token'
        assert example_client.config == example_config

    def test_constructor_no_token_no_config(self):
        example_token = 'token'
        example_config = MediaConfig()

        with pytest.raises(ValueError):
            RevAiStreamingClient(example_token, None)
        with pytest.raises(ValueError):
            RevAiStreamingClient(None, example_config)

    def test_start_success(self, mock_streaming_client, mock_generator, capsys):
        metadata = "my metadata"
        url = mock_streaming_client.base_url + \
            '?access_token={}'.format(mock_streaming_client.access_token) + \
            '&content_type={}'. \
            format(mock_streaming_client.config.get_content_type_string()) + \
            '&user_agent={}'.format(quote('RevAi-PythonSDK/{}'.format(__version__), safe='')) + \
            '&metadata={}'.format(quote(metadata))
        example_data = '{"type":"partial","transcript":"Test"}'
        example_connected = '{"type":"connected","id":"testid"}'
        if six.PY3:
            example_data = example_data.encode('utf-8')
            example_connected = example_connected.encode('utf-8')
        data = [
            [0x1, example_connected],
            [0x1, example_data],
            [0x8, b'\x03\xe8End of input. Closing']
        ]
        exp_responses = [
            'Connected, Job ID : testid\n',
            '{"type":"partial","transcript":"Test"}',
            'Connection Closed. Code : 1000; Reason : End of input. Closing\n'
        ]
        mock_streaming_client.client.recv_data.side_effect = data

        response_gen = mock_streaming_client.start(mock_generator(), metadata)

        mock_streaming_client.client.connect.assert_called_once_with(url)
        mock_streaming_client.client.send_binary.assert_any_call(0)
        mock_streaming_client.client.send_binary.assert_any_call(1)
        mock_streaming_client.client.send_binary.assert_any_call(2)
        assert hasattr(mock_streaming_client, 'request_thread')
        for ind, response in enumerate(response_gen):
            assert capsys.readouterr().out == exp_responses[ind]
            assert exp_responses[ind + 1] == response
        assert capsys.readouterr().out == exp_responses[2]

    def test_start_failure_to_connect(self, mock_streaming_client, mock_generator):
        mock_streaming_client.client.connect = lambda x: 1 / 0

        with pytest.raises(ZeroDivisionError):
            mock_streaming_client.start(mock_generator())

    def test_end(self, mock_streaming_client):
        mock_streaming_client.end()

        mock_streaming_client.client.abort.assert_called_once_with()
