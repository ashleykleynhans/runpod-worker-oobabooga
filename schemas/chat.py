# OpenAI-compatible chat completions schema for /v1/chat/completions endpoint
CHAT_SCHEMA = {
    'model': {
        'type': str,
        'required': False,
        'default': None,
    },
    'messages': {
        'type': list,
        'required': True
    },
    'max_tokens': {
        'type': int,
        'required': False,
        'default': 250,
    },
    'temperature': {
        'type': float,
        'required': False,
        'default': 0.7,
    },
    'top_p': {
        'type': float,
        'required': False,
        'default': 0.9,
    },
    'top_k': {
        'type': int,
        'required': False,
        'default': 20,
    },
    'stream': {
        'type': bool,
        'required': False,
        'default': False,
    },
    'stop': {
        'type': list,
        'required': False,
        'default': [],
    },
    'frequency_penalty': {
        'type': float,
        'required': False,
        'default': 0,
    },
    'presence_penalty': {
        'type': float,
        'required': False,
        'default': 0,
    },
    'seed': {
        'type': int,
        'required': False,
        'default': -1,
    },
    # Additional OpenAI-compatible parameters
    'n': {
        'type': int,
        'required': False,
        'default': 1,
    },
    'max_completion_tokens': {
        'type': int,
        'required': False,
        'default': None,
    },
    'logprobs': {
        'type': bool,
        'required': False,
        'default': False,
    },
    'top_logprobs': {
        'type': int,
        'required': False,
        'default': None,
    },
    'logit_bias': {
        'type': dict,
        'required': False,
        'default': None,
    },
    'response_format': {
        'type': dict,
        'required': False,
        'default': None,
    },
    'tools': {
        'type': list,
        'required': False,
        'default': None,
    },
    'tool_choice': {
        'type': (str, dict),
        'required': False,
        'default': None,
    },
    'user': {
        'type': str,
        'required': False,
        'default': None,
    },
    # Oobabooga-specific parameters
    'mode': {
        'type': str,
        'required': False,
        'default': 'instruct',
        'constraints': lambda mode: mode in [
            'instruct',
            'chat',
            'chat-instruct',
        ]
    },
    'character': {
        'type': str,
        'required': False,
        'default': None,
    },
    'instruction_template': {
        'type': str,
        'required': False,
        'default': None,
    },
}
