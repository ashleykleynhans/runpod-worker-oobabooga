# Completions API

OpenAI-compatible text completions endpoint for text generation.

## Request

```json
{
  "input": {
    "api": {
      "method": "POST",
      "endpoint": "completions"
    },
    "payload": {
      "prompt": "In order to make homemade bread, follow these steps:\n1)",
      "max_tokens": 250
    }
  }
}
```

## Payload Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| prompt | string | Yes | - | The prompt to complete |
| max_tokens | int | No | 250 | Maximum number of tokens to generate |
| temperature | float | No | 0.7 | Sampling temperature (0.0-2.0) |
| top_p | float | No | 0.9 | Nucleus sampling parameter |
| top_k | int | No | 20 | Top-k sampling parameter |
| stream | bool | No | false | Enable streaming responses |
| stop | array | No | [] | Stop sequences |
| frequency_penalty | float | No | 0 | Frequency penalty (-2.0 to 2.0) |
| presence_penalty | float | No | 0 | Presence penalty (-2.0 to 2.0) |
| seed | int | No | -1 | Random seed (-1 for random) |

## Response

### RUN (async)

```json
{
    "id": "83bbc301-5dcd-4236-9293-a65cdd681858",
    "status": "IN_QUEUE"
}
```

### RUNSYNC (sync)

```json
{
    "delayTime": 15318,
    "executionTime": 27809,
    "id": "sync-ce2d3e58-6168-49c1-a038-9c62b369ae1e",
    "output": {
        "id": "cmpl-abc123",
        "object": "text_completion",
        "created": 1703123456,
        "model": "text-generation-webui",
        "choices": [
            {
                "index": 0,
                "text": " Mix the dry ingredients together in a large bowl. This includes flour, yeast, salt and any other spices you may want to add. Make sure that all of your ingredients are well mixed before moving on to step 2).",
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 15,
            "completion_tokens": 52,
            "total_tokens": 67
        }
    },
    "status": "COMPLETED"
}
```
