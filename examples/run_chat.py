#!/usr/bin/env python3
import json
from util import post_request


def get_response_output(resp_json):
    if resp_json:
        if 'output' in resp_json:
            output = resp_json['output']
            if 'choices' in output and len(output['choices']):
                message = output['choices'][0].get('message', {})
                print(message.get('content', ''))
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
                "endpoint": "chat/completions"
            },
            "payload": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Please give me a step-by-step guide on how to plant a tree in my backyard."
                    }
                ],
                "max_tokens": 2000
            }
        }
    }

    get_response_output(post_request(payload))
