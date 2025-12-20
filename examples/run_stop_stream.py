#!/usr/bin/env python3
import json
from util import post_request


def get_response_output(resp_json):
    if resp_json:
        if 'output' in resp_json:
            print(resp_json['output']['results'])
        else:
            print(json.dumps(resp_json, indent=4, default=str))


if __name__ == '__main__':
    payload = {
        "input": {
            "api": {
                "method": "POST",
                "endpoint": "/stop-stream"
            },
            "payload": {
            }
        }
    }

    get_response_output(post_request(payload))
