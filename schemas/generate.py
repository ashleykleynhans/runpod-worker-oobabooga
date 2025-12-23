# OpenAI-compatible completions schema for /v1/completions endpoint
COMPLETIONS_SCHEMA = {
    'model': {
        'type': str,
        'required': False,
        'default': None,
    },
    'prompt': {
        'type': str,
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
    'suffix': {
        'type': str,
        'required': False,
        'default': None,
    },
    'n': {
        'type': int,
        'required': False,
        'default': 1,
    },
    'logprobs': {
        'type': int,
        'required': False,
        'default': None,
    },
    'echo': {
        'type': bool,
        'required': False,
        'default': False,
    },
    'best_of': {
        'type': int,
        'required': False,
        'default': 1,
    },
    'logit_bias': {
        'type': dict,
        'required': False,
        'default': None,
    },
    'user': {
        'type': str,
        'required': False,
        'default': None,
    },
}
