import time
import requests
from dotenv import dotenv_values

STATUS_IN_QUEUE = 'IN_QUEUE'
STATUS_IN_PROGRESS = 'IN_PROGRESS'
STATUS_FAILED = 'FAILED'
STATUS_CANCELLED = 'CANCELLED'
STATUS_COMPLETED = 'COMPLETED'
STATUS_TIMED_OUT = 'TIMED_OUT'


class Timer:
    def __init__(self):
        self.start = time.time()

    def restart(self):
        self.start = time.time()

    def get_elapsed_time(self):
        end = time.time()
        return round(end - self.start, 1)


def handle_response(resp_json, timer):
    total_time = timer.get_elapsed_time()
    print(f'Total time taken for RunPod Serverless API call {total_time} seconds')
    return resp_json


def post_request(payload, runtype='run'):
    timer = Timer()
    env = dotenv_values('.env')
    runpod_api_key = env.get('RUNPOD_API_KEY', None)
    runpod_endpoint_id = env.get('RUNPOD_ENDPOINT_ID', None)

    if runpod_api_key is not None and runpod_endpoint_id is not None:
        base_url = f'https://api.runpod.ai/v2/{runpod_endpoint_id}'
    else:
        base_url = f'http://127.0.0.1:8000'

    r = requests.post(
        f'{base_url}/{runtype}',
        headers={
            'Authorization': f'Bearer {runpod_api_key}'
        },
        json=payload
    )

    print(f'Status code: {r.status_code}')

    if r.status_code == 200:
        resp_json = r.json()

        if 'output' in resp_json:
            return handle_response(resp_json, timer)
        else:
            job_status = resp_json.get('status', STATUS_FAILED)
            print(f'Job status: {job_status}')

            if job_status == STATUS_IN_QUEUE or job_status == STATUS_IN_PROGRESS:
                request_id = resp_json['id']
                request_in_queue = True

                while request_in_queue:
                    r = requests.get(
                        f'{base_url}/status/{request_id}',
                        headers={
                            'Authorization': f'Bearer {runpod_api_key}'
                        },
                    )

                    print(f'Status code from RunPod status endpoint: {r.status_code}')

                    if r.status_code == 200:
                        resp_json = r.json()
                        job_status = resp_json['status']

                        if job_status == STATUS_IN_QUEUE or job_status == STATUS_IN_PROGRESS:
                            print(f'RunPod request {request_id} is {job_status}, sleeping for 5 seconds...')
                            time.sleep(5)
                        elif job_status == STATUS_CANCELLED:
                            print(f'RunPod request {request_id} cancelled')
                            return handle_response(resp_json, timer)
                        elif job_status == STATUS_FAILED:
                            print(f'RunPod request {request_id} failed')
                            return handle_response(resp_json, timer)
                        elif job_status == STATUS_COMPLETED:
                            print(f'RunPod request {request_id} completed')
                            return handle_response(resp_json, timer)
                        elif job_status == STATUS_TIMED_OUT:
                            print(f'ERROR: RunPod request {request_id} timed out')
                            return handle_response(resp_json, timer)
                        else:
                            print(f'ERROR: Invalid status response from RunPod status endpoint')
                            return handle_response(resp_json, timer)
            else:
                return handle_response(resp_json, timer)
    else:
        print(f'ERROR: {r.content}')
