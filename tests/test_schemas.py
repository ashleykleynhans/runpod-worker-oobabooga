"""Tests for validation schemas."""
import pytest
from schemas.api import API_SCHEMA
from schemas.chat import CHAT_SCHEMA
from schemas.generate import COMPLETIONS_SCHEMA
from schemas.model import MODEL_SCHEMA


class TestAPISchema:
    """Tests for API_SCHEMA."""

    def test_api_schema_has_required_fields(self):
        """Test that API_SCHEMA has method and endpoint fields."""
        assert 'method' in API_SCHEMA
        assert 'endpoint' in API_SCHEMA

    def test_method_field_config(self):
        """Test method field configuration."""
        method = API_SCHEMA['method']
        assert method['type'] == str
        assert method['required'] is True
        assert 'constraints' in method

    def test_method_constraints_valid(self):
        """Test that valid methods pass constraints."""
        constraint = API_SCHEMA['method']['constraints']
        assert constraint('GET') is True
        assert constraint('POST') is True

    def test_method_constraints_invalid(self):
        """Test that invalid methods fail constraints."""
        constraint = API_SCHEMA['method']['constraints']
        assert constraint('PUT') is False
        assert constraint('DELETE') is False
        assert constraint('PATCH') is False

    def test_endpoint_field_config(self):
        """Test endpoint field configuration."""
        endpoint = API_SCHEMA['endpoint']
        assert endpoint['type'] == str
        assert endpoint['required'] is True
        assert 'constraints' in endpoint

    def test_endpoint_constraints_valid(self):
        """Test that valid endpoints pass constraints."""
        constraint = API_SCHEMA['endpoint']['constraints']
        assert constraint('completions') is True
        assert constraint('chat/completions') is True
        assert constraint('models') is True
        assert constraint('internal/model/load') is True
        assert constraint('internal/model/list') is True

    def test_endpoint_constraints_invalid(self):
        """Test that invalid endpoints fail constraints."""
        constraint = API_SCHEMA['endpoint']['constraints']
        assert constraint('invalid') is False
        assert constraint('api/v1/generate') is False


class TestCompletionsSchema:
    """Tests for COMPLETIONS_SCHEMA."""

    def test_completions_schema_has_prompt(self):
        """Test that COMPLETIONS_SCHEMA has required prompt field."""
        assert 'prompt' in COMPLETIONS_SCHEMA
        assert COMPLETIONS_SCHEMA['prompt']['type'] == str
        assert COMPLETIONS_SCHEMA['prompt']['required'] is True

    def test_completions_schema_optional_fields(self):
        """Test optional fields have correct defaults."""
        assert COMPLETIONS_SCHEMA['max_tokens']['default'] == 250
        assert COMPLETIONS_SCHEMA['temperature']['default'] == 0.7
        assert COMPLETIONS_SCHEMA['top_p']['default'] == 0.9
        assert COMPLETIONS_SCHEMA['top_k']['default'] == 20
        assert COMPLETIONS_SCHEMA['stream']['default'] is False
        assert COMPLETIONS_SCHEMA['stop']['default'] == []
        assert COMPLETIONS_SCHEMA['frequency_penalty']['default'] == 0
        assert COMPLETIONS_SCHEMA['presence_penalty']['default'] == 0
        assert COMPLETIONS_SCHEMA['seed']['default'] == -1

    def test_completions_schema_optional_fields_not_required(self):
        """Test optional fields are not required."""
        optional_fields = [
            'max_tokens', 'temperature', 'top_p', 'top_k',
            'stream', 'stop', 'frequency_penalty', 'presence_penalty', 'seed'
        ]
        for field in optional_fields:
            assert COMPLETIONS_SCHEMA[field]['required'] is False


class TestChatSchema:
    """Tests for CHAT_SCHEMA."""

    def test_chat_schema_has_messages(self):
        """Test that CHAT_SCHEMA has required messages field."""
        assert 'messages' in CHAT_SCHEMA
        assert CHAT_SCHEMA['messages']['type'] == list
        assert CHAT_SCHEMA['messages']['required'] is True

    def test_chat_schema_has_mode(self):
        """Test that CHAT_SCHEMA has mode field with constraints."""
        assert 'mode' in CHAT_SCHEMA
        mode = CHAT_SCHEMA['mode']
        assert mode['type'] == str
        assert mode['required'] is False
        assert mode['default'] == 'instruct'

    def test_mode_constraints_valid(self):
        """Test that valid modes pass constraints."""
        constraint = CHAT_SCHEMA['mode']['constraints']
        assert constraint('instruct') is True
        assert constraint('chat') is True
        assert constraint('chat-instruct') is True

    def test_mode_constraints_invalid(self):
        """Test that invalid modes fail constraints."""
        constraint = CHAT_SCHEMA['mode']['constraints']
        assert constraint('invalid') is False
        assert constraint('completion') is False

    def test_chat_schema_optional_fields(self):
        """Test optional fields have correct defaults."""
        assert CHAT_SCHEMA['max_tokens']['default'] == 250
        assert CHAT_SCHEMA['temperature']['default'] == 0.7


class TestModelSchema:
    """Tests for MODEL_SCHEMA."""

    def test_model_schema_has_model_name(self):
        """Test that MODEL_SCHEMA has required model_name field."""
        assert 'model_name' in MODEL_SCHEMA
        assert MODEL_SCHEMA['model_name']['type'] == str
        assert MODEL_SCHEMA['model_name']['required'] is True

    def test_model_schema_optional_fields(self):
        """Test optional fields have correct defaults."""
        assert MODEL_SCHEMA['args']['default'] == {}
        assert MODEL_SCHEMA['settings']['default'] == {}
        assert MODEL_SCHEMA['args']['required'] is False
        assert MODEL_SCHEMA['settings']['required'] is False
