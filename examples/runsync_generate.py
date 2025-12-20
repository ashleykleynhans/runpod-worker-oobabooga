#!/usr/bin/env python3
import json
from util import post_request


def get_response_output(resp_json):
    if resp_json:
        if 'output' in resp_json:
            results = resp_json['output']['results']

            if len(results):
                print(results[0]['text'])
            else:
                print('No results output received from endpoint')
                print(json.dumps(resp_json, indent=4, default=str))
        else:
            print(json.dumps(resp_json, indent=4, default=str))


if __name__ == '__main__':
    payload = {
        "input": {
            "api": {
                "method": "POST",
                "endpoint": "/generate"
            },
            "payload": {
                "prompt": "In order to make homemade bread, follow these steps:\n1)"
            }
        }
    }

    get_response_output(post_request(payload, 'runsync'))
