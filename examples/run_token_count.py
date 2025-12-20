#!/usr/bin/env python3
import json
from util import post_request


def get_response_output(resp_json):
    if resp_json:
        if 'output' in resp_json:
            result = resp_json['output']['results']

            if len(result):
                print(result[0]['tokens'])
        else:
            print(json.dumps(resp_json, indent=4, default=str))


if __name__ == '__main__':
    payload = {
        "input": {
            "api": {
                "method": "POST",
                "endpoint": "/token-count"
            },
            "payload": {
                "prompt": "Please give me a step-by-step guide on how to plant a tree in my backyard."
            }
        }
    }

    get_response_output(post_request(payload))
