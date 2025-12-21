# List Models API

OpenAI-compatible endpoint to list available models.

## Request

```json
{
  "input": {
    "api": {
      "method": "GET",
      "endpoint": "models"
    },
    "payload": {}
  }
}
```

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
    "delayTime": 27982,
    "executionTime": 307,
    "id": "sync-4b4a8565-0018-4802-a453-b336f9d332d7",
    "output": {
        "object": "list",
        "data": [
            {
                "id": "TheBloke_Pygmalion-13B-SuperHOT-8K-GPTQ",
                "object": "model",
                "created": 1703123456,
                "owned_by": "text-generation-webui"
            }
        ]
    },
    "status": "COMPLETED"
}
```
