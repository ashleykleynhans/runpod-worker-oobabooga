import json
import time
import requests
import runpod
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.modules.rp_logger import RunPodLogger
from requests.adapters import HTTPAdapter, Retry
from schemas.api import API_SCHEMA
from schemas.chat import CHAT_SCHEMA
from schemas.generate import COMPLETIONS_SCHEMA
from schemas.model import MODEL_SCHEMA

BASE_URI = 'http://127.0.0.1:5000'
TIMEOUT = 600

# Endpoint mapping from user-friendly names to OpenAI API paths
ENDPOINT_MAPPING = {
    'completions': '/v1/completions',
    'chat/completions': '/v1/chat/completions',
    'models': '/v1/models',
    'internal/model/load': '/v1/internal/model/load',
    'internal/model/list': '/v1/internal/model/list',
}

VALIDATION_SCHEMAS = {
    'completions': COMPLETIONS_SCHEMA,
    'chat/completions': CHAT_SCHEMA,
}

session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
logger = RunPodLogger()


# ---------------------------------------------------------------------------- #
# Application Functions                                                        #
# ---------------------------------------------------------------------------- #
def wait_for_service(url):
    retries = 0

    while True:
        try:
            requests.get(url)
            return
        except requests.exceptions.RequestException:
            retries += 1

            # Only log every 15 retries so the logs don't get spammed
            if retries % 15 == 0:
                logger.info('Service not ready yet. Retrying...')
        except Exception as err:
            logger.error(f'Error: {err}')

        time.sleep(0.2)


def send_get_request(endpoint):
    return session.get(
        url=f'{BASE_URI}{endpoint}',
        timeout=TIMEOUT
    )


def send_post_request(endpoint, payload):
    return session.post(
        url=f'{BASE_URI}{endpoint}',
        json=payload,
        timeout=TIMEOUT
    )


def validate_api(event):
    if 'api' not in event['input']:
        return {
            'errors': '"api" is a required field in the "input" payload'
        }

    api = event['input']['api']

    if type(api) is not dict:
        return {
            'errors': '"api" must be a dictionary containing "method" and "endpoint"'
        }

    api['endpoint'] = api['endpoint'].lstrip('/')

    return validate(api, API_SCHEMA)


def validate_payload(event):
    method = event['input']['api']['method']
    endpoint = event['input']['api']['endpoint']
    payload = event['input'].get('payload', {})
    validated_input = {}

    if endpoint in VALIDATION_SCHEMAS:
        validated_input = validate(payload, VALIDATION_SCHEMAS[endpoint])
    elif endpoint == 'internal/model/load':
        validated_input = validate(payload, MODEL_SCHEMA)

    return endpoint, method, validated_input


# ---------------------------------------------------------------------------- #
# Runpod Handler                                                               #
# ---------------------------------------------------------------------------- #
def handler(event):
    validated_api = validate_api(event)

    if 'errors' in validated_api:
        return {
            'error': ','.join(validated_api['errors'])
        }

    endpoint, method, validated_input = validate_payload(event)

    if 'errors' in validated_input:
        return {
            'error': ','.join(validated_input['errors'])
        }

    if 'validated_input' in validated_input:
        payload = validated_input['validated_input']
    else:
        payload = event['input'].get('payload', {})

    # Map to actual OpenAI API endpoint path
    api_path = ENDPOINT_MAPPING.get(endpoint, f'/v1/{endpoint}')

    try:
        logger.log(f'Sending {method} request to: {api_path}')

        if method == 'GET':
            response = send_get_request(api_path)
        elif method == 'POST':
            response = send_post_request(api_path, payload)
    except Exception as e:
        return {
            'error': str(e)
        }

    return response.json()


if __name__ == '__main__':
    wait_for_service(url=f'{BASE_URI}/v1/models')
    logger.log('Oobabooga API is ready', 'INFO')
    logger.log('Starting Runpod Serverless...', 'INFO')
    runpod.serverless.start(
        {
            'handler': handler
        }
    )
