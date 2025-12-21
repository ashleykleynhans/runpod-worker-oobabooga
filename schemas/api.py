API_SCHEMA = {
    'method': {
        'type': str,
        'required': True,
        'constraints': lambda method: method in [
            'GET',
            'POST'
        ]
    },
    'endpoint': {
        'type': str,
        'required': True,
        'constraints': lambda endpoint: endpoint in [
            'completions',
            'chat/completions',
            'models',
            'internal/model/load',
            'internal/model/list'
        ]
    }
}
