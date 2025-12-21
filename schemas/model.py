# Schema for /v1/internal/model/load endpoint
MODEL_SCHEMA = {
    'model_name': {
        'type': str,
        'required': True,
    },
    'args': {
        'type': dict,
        'required': False,
        'default': {}
    },
    'settings': {
        'type': dict,
        'required': False,
        'default': {}
    }
}
