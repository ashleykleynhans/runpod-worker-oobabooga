# Load Model API

Internal endpoint to load a model into memory.

## Request

```json
{
  "input": {
    "api": {
      "method": "POST",
      "endpoint": "internal/model/load"
    },
    "payload": {
      "model_name": "Qwen_Qwen2.5-7B-Instruct",
      "args": {},
      "settings": {}
    }
  }
}
```

## Payload Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| model_name | string | Yes | - | Name of the model to load |
| args | object | No | {} | Model loading arguments |
| settings | object | No | {} | Model settings |

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
    "delayTime": 3451,
    "executionTime": 3655,
    "id": "sync-a6c22f66-7baf-46cf-8476-4f207ef2d913",
    "output": "OK",
    "status": "COMPLETED",
    "workerId": "vdu7ciz2x4tm4o" 
}
```
