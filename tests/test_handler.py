"""Tests for the handler module."""
import pytest
import responses
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import (
    validate_api,
    validate_payload,
    handler,
    send_get_request,
    send_post_request,
    wait_for_service,
    ENDPOINT_MAPPING,
    BASE_URI,
)


class TestValidateApi:
    """Tests for validate_api function."""

    def test_missing_api_field(self):
        """Test error when api field is missing."""
        event = {'input': {}}
        result = validate_api(event)
        assert 'errors' in result
        assert '"api" is a required field' in result['errors']

    def test_api_not_dict(self):
        """Test error when api is not a dictionary."""
        event = {'input': {'api': 'not a dict'}}
        result = validate_api(event)
        assert 'errors' in result
        assert '"api" must be a dictionary' in result['errors']

    def test_valid_api_get(self):
        """Test valid GET request passes validation."""
        event = {
            'input': {
                'api': {
                    'method': 'GET',
                    'endpoint': 'models'
                }
            }
        }
        result = validate_api(event)
        assert 'errors' not in result or len(result.get('errors', [])) == 0

    def test_valid_api_post(self):
        """Test valid POST request passes validation."""
        event = {
            'input': {
                'api': {
                    'method': 'POST',
                    'endpoint': 'completions'
                }
            }
        }
        result = validate_api(event)
        assert 'errors' not in result or len(result.get('errors', [])) == 0

    def test_endpoint_leading_slash_stripped(self):
        """Test that leading slashes are stripped from endpoint."""
        event = {
            'input': {
                'api': {
                    'method': 'GET',
                    'endpoint': '/models'
                }
            }
        }
        validate_api(event)
        assert event['input']['api']['endpoint'] == 'models'


class TestValidatePayload:
    """Tests for validate_payload function."""

    def test_completions_endpoint_validation(self):
        """Test that completions endpoint uses COMPLETIONS_SCHEMA."""
        event = {
            'input': {
                'api': {
                    'method': 'POST',
                    'endpoint': 'completions'
                },
                'payload': {
                    'prompt': 'Hello world'
                }
            }
        }
        endpoint, method, validated = validate_payload(event)
        assert endpoint == 'completions'
        assert method == 'POST'

    def test_chat_completions_endpoint_validation(self):
        """Test that chat/completions endpoint uses CHAT_SCHEMA."""
        event = {
            'input': {
                'api': {
                    'method': 'POST',
                    'endpoint': 'chat/completions'
                },
                'payload': {
                    'messages': [{'role': 'user', 'content': 'Hello'}]
                }
            }
        }
        endpoint, method, validated = validate_payload(event)
        assert endpoint == 'chat/completions'
        assert method == 'POST'

    def test_model_load_endpoint_validation(self):
        """Test that internal/model/load endpoint uses MODEL_SCHEMA."""
        event = {
            'input': {
                'api': {
                    'method': 'POST',
                    'endpoint': 'internal/model/load'
                },
                'payload': {
                    'model_name': 'test-model'
                }
            }
        }
        endpoint, method, validated = validate_payload(event)
        assert endpoint == 'internal/model/load'
        assert method == 'POST'

    def test_no_payload_uses_empty_dict(self):
        """Test that missing payload defaults to empty dict."""
        event = {
            'input': {
                'api': {
                    'method': 'GET',
                    'endpoint': 'models'
                }
            }
        }
        endpoint, method, validated = validate_payload(event)
        assert endpoint == 'models'


class TestEndpointMapping:
    """Tests for endpoint mapping."""

    def test_all_endpoints_mapped(self):
        """Test that all expected endpoints are in the mapping."""
        expected = [
            'completions',
            'chat/completions',
            'models',
            'internal/model/load',
            'internal/model/list',
        ]
        for endpoint in expected:
            assert endpoint in ENDPOINT_MAPPING

    def test_endpoint_paths_correct(self):
        """Test that endpoints map to correct OpenAI API paths."""
        assert ENDPOINT_MAPPING['completions'] == '/v1/completions'
        assert ENDPOINT_MAPPING['chat/completions'] == '/v1/chat/completions'
        assert ENDPOINT_MAPPING['models'] == '/v1/models'
        assert ENDPOINT_MAPPING['internal/model/load'] == '/v1/internal/model/load'
        assert ENDPOINT_MAPPING['internal/model/list'] == '/v1/internal/model/list'


class TestSendRequests:
    """Tests for send_get_request and send_post_request."""

    @responses.activate
    def test_send_get_request(self):
        """Test sending GET request."""
        responses.add(
            responses.GET,
            f'{BASE_URI}/v1/models',
            json={'data': []},
            status=200
        )
        response = send_get_request('/v1/models')
        assert response.status_code == 200
        assert response.json() == {'data': []}

    @responses.activate
    def test_send_post_request(self):
        """Test sending POST request."""
        responses.add(
            responses.POST,
            f'{BASE_URI}/v1/completions',
            json={'choices': [{'text': 'Hello'}]},
            status=200
        )
        response = send_post_request('/v1/completions', {'prompt': 'Hi'})
        assert response.status_code == 200
        assert 'choices' in response.json()


class TestHandler:
    """Tests for the main handler function."""

    def test_handler_missing_api(self):
        """Test handler returns error when api is missing."""
        event = {'input': {}}
        result = handler(event)
        assert 'error' in result

    def test_handler_invalid_api_type(self):
        """Test handler returns error when api is not a dict."""
        event = {'input': {'api': 'invalid'}}
        result = handler(event)
        assert 'error' in result

    @responses.activate
    def test_handler_get_models(self):
        """Test handler successfully processes GET models request."""
        responses.add(
            responses.GET,
            f'{BASE_URI}/v1/models',
            json={'data': [{'id': 'test-model'}]},
            status=200
        )
        event = {
            'input': {
                'api': {
                    'method': 'GET',
                    'endpoint': 'models'
                }
            }
        }
        result = handler(event)
        assert 'data' in result
        assert result['data'][0]['id'] == 'test-model'

    @responses.activate
    def test_handler_post_completions(self):
        """Test handler successfully processes POST completions request."""
        responses.add(
            responses.POST,
            f'{BASE_URI}/v1/completions',
            json={
                'choices': [{'text': 'Generated text'}],
                'usage': {'total_tokens': 10}
            },
            status=200
        )
        event = {
            'input': {
                'api': {
                    'method': 'POST',
                    'endpoint': 'completions'
                },
                'payload': {
                    'prompt': 'Hello'
                }
            }
        }
        result = handler(event)
        assert 'choices' in result

    @responses.activate
    def test_handler_post_chat_completions(self):
        """Test handler successfully processes POST chat/completions request."""
        responses.add(
            responses.POST,
            f'{BASE_URI}/v1/chat/completions',
            json={
                'choices': [{'message': {'content': 'Hello!'}}]
            },
            status=200
        )
        event = {
            'input': {
                'api': {
                    'method': 'POST',
                    'endpoint': 'chat/completions'
                },
                'payload': {
                    'messages': [{'role': 'user', 'content': 'Hi'}]
                }
            }
        }
        result = handler(event)
        assert 'choices' in result

    @responses.activate
    def test_handler_request_exception(self):
        """Test handler returns error on request exception."""
        responses.add(
            responses.GET,
            f'{BASE_URI}/v1/models',
            body=Exception('Connection error')
        )
        event = {
            'input': {
                'api': {
                    'method': 'GET',
                    'endpoint': 'models'
                }
            }
        }
        result = handler(event)
        assert 'error' in result

    @responses.activate
    def test_handler_uses_validated_input(self):
        """Test handler uses validated input with defaults applied."""
        responses.add(
            responses.POST,
            f'{BASE_URI}/v1/completions',
            json={'choices': []},
            status=200
        )
        event = {
            'input': {
                'api': {
                    'method': 'POST',
                    'endpoint': 'completions'
                },
                'payload': {
                    'prompt': 'Test'
                }
            }
        }
        result = handler(event)
        # Verify request was made (no error)
        assert 'error' not in result

    def test_handler_payload_validation_error(self):
        """Test handler returns error when payload validation fails."""
        event = {
            'input': {
                'api': {
                    'method': 'POST',
                    'endpoint': 'completions'
                },
                'payload': {
                    # Missing required 'prompt' field
                    'max_tokens': 100
                }
            }
        }
        result = handler(event)
        assert 'error' in result
        assert 'prompt' in result['error'].lower() or 'required' in result['error'].lower()


class TestWaitForService:
    """Tests for wait_for_service function."""

    @responses.activate
    def test_wait_for_service_success_immediately(self):
        """Test wait_for_service returns when service is available."""
        responses.add(
            responses.GET,
            f'{BASE_URI}/v1/models',
            json={'data': []},
            status=200
        )
        # Should return without error
        wait_for_service(f'{BASE_URI}/v1/models')
        assert len(responses.calls) == 1

    @patch('handler.time.sleep')
    @patch('handler.requests.get')
    def test_wait_for_service_retries_on_request_exception(self, mock_get, mock_sleep):
        """Test wait_for_service retries on RequestException."""
        import requests as req
        # Fail twice, then succeed
        mock_get.side_effect = [
            req.exceptions.ConnectionError(),
            req.exceptions.ConnectionError(),
            MagicMock(status_code=200)
        ]
        wait_for_service(f'{BASE_URI}/v1/models')
        assert mock_get.call_count == 3
        assert mock_sleep.call_count == 2

    @patch('handler.time.sleep')
    @patch('handler.requests.get')
    @patch('handler.logger')
    def test_wait_for_service_logs_every_15_retries(self, mock_logger, mock_get, mock_sleep):
        """Test wait_for_service logs every 15 retries."""
        import requests as req
        # Fail 15 times, then succeed
        failures = [req.exceptions.ConnectionError() for _ in range(15)]
        mock_get.side_effect = failures + [MagicMock(status_code=200)]
        wait_for_service(f'{BASE_URI}/v1/models')
        assert mock_get.call_count == 16
        # Should have logged once at retry 15
        mock_logger.info.assert_called_once_with('Service not ready yet. Retrying...')

    @patch('handler.time.sleep')
    @patch('handler.requests.get')
    @patch('handler.logger')
    def test_wait_for_service_logs_generic_exception(self, mock_logger, mock_get, mock_sleep):
        """Test wait_for_service logs generic exceptions."""
        # Fail with generic exception, then succeed
        mock_get.side_effect = [
            ValueError('Some error'),
            MagicMock(status_code=200)
        ]
        wait_for_service(f'{BASE_URI}/v1/models')
        assert mock_get.call_count == 2
        mock_logger.error.assert_called_once()
        assert 'Some error' in str(mock_logger.error.call_args)
