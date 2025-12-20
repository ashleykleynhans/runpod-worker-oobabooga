#!/usr/bin/env python3
import json
from util import post_request


def get_response_output(resp_json):
    if resp_json:
        if 'output' in resp_json:
            print(resp_json['output']['result'])
        else:
            print(json.dumps(resp_json, indent=4, default=str))


if __name__ == '__main__':
    payload = {
        "input": {
            "api": {
                "method": "GET",
                "endpoint": "/model"
            },
            "payload": {
            }
        }
    }

    get_response_output(post_request(payload, 'runsync'))
