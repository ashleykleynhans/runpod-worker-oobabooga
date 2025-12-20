import json
import time
import requests
import runpod
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.modules.rp_logger import RunPodLogger
from requests.adapters import HTTPAdapter, Retry
from schemas.api import API_SCHEMA
from schemas.chat import CHAT_SCHEMA
from schemas.generate import GENERATE_SCHEMA
from schemas.token_count import TOKEN_COUNT_SCHEMA
from schemas.model import MODEL_SCHEMA

BASE_URI = 'http://127.0.0.1:5000/api/v1'
TIMEOUT = 600

VALIDATION_SCHEMAS = {
    'chat': CHAT_SCHEMA,
    'generate': GENERATE_SCHEMA,
    'token-count': TOKEN_COUNT_SCHEMA
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
        url=f'{BASE_URI}/{endpoint}',
        timeout=TIMEOUT
    )


def send_post_request(endpoint, payload):
    return session.post(
        url=f'{BASE_URI}/{endpoint}',
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
    payload = event['input']['payload']
    validated_input = {}

    if endpoint == 'generate':
        validated_input = validate(payload, GENERATE_SCHEMA)
    elif endpoint == 'chat':
        validated_input = validate(payload, CHAT_SCHEMA)
    elif endpoint == 'token-count':
        validated_input = validate(payload, TOKEN_COUNT_SCHEMA)
    elif endpoint == 'model' and method == 'POST':
        validated_input = validate(payload, MODEL_SCHEMA)

    return endpoint, event['input']['api']['method'], validated_input


# ---------------------------------------------------------------------------- #
# RunPod Handler                                                               #
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
        payload = {}

    try:
        logger.log(f'Sending {method} request to: {endpoint}')

        if method == 'GET':
            response = send_post_request(endpoint, payload)
        elif method == 'POST':
            response = send_post_request(endpoint, payload)
    except Exception as e:
        return {
            'error': str(e)
        }

    return response.json()


if __name__ == '__main__':
    wait_for_service(url=f'{BASE_URI}/model')
    logger.log('Oobabooga API is ready', 'INFO')
    logger.log('Starting RunPod Serverless...', 'INFO')
    runpod.serverless.start(
        {
            'handler': handler
        }
    )
