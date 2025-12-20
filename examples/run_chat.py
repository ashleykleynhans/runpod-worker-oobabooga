#!/usr/bin/env python3
import json
from util import post_request


def get_response_output(resp_json):
    if resp_json:
        if 'output' in resp_json:
            result = resp_json['output']['results'][0]['history']

            if len(result['visible']):
                print(result['visible'][-1][1])
            else:
                print('No visible output received from endpoint')
                print(json.dumps(resp_json, indent=4, default=str))
        else:
            print(json.dumps(resp_json, indent=4, default=str))


if __name__ == '__main__':
    payload = {
        "input": {
            "api": {
                "method": "POST",
                "endpoint": "/chat"
            },
            "payload": {
                "user_input": "Please give me a step-by-step guide on how to plant a tree in my backyard.",
                "max_new_tokens": 250
            }
        }
    }

    get_response_output(post_request(payload))
