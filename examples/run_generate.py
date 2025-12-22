#!/usr/bin/env python3
import json
from util import post_request


def get_response_output(resp_json):
    if resp_json:
        if 'output' in resp_json:
            output = resp_json['output']
            if 'choices' in output and len(output['choices']):
                print(output['choices'][0]['text'])
            else:
                print('No choices received from endpoint')
                print(json.dumps(resp_json, indent=4, default=str))
        else:
            print(json.dumps(resp_json, indent=4, default=str))


if __name__ == '__main__':
    payload = {
        "input": {
            "api": {
                "method": "POST",
                "endpoint": "completions"
            },
            "payload": {
                "prompt": "In order to make homemade bread, follow these steps:\n1)",
                "max_tokens": 1000
            }
        }
    }

    get_response_output(post_request(payload))
