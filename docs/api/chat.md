# Chat Completions API

OpenAI-compatible chat completions endpoint for conversational interactions.

## Request

```json
{
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
      "max_tokens": 250
    }
  }
}
```

## Payload Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| messages | array | Yes | - | Array of message objects with `role` and `content` |
| max_tokens | int | No | 250 | Maximum number of tokens to generate |
| temperature | float | No | 0.7 | Sampling temperature (0.0-2.0) |
| top_p | float | No | 0.9 | Nucleus sampling parameter |
| top_k | int | No | 20 | Top-k sampling parameter |
| stream | bool | No | false | Enable streaming responses |
| stop | array | No | [] | Stop sequences |
| frequency_penalty | float | No | 0 | Frequency penalty (-2.0 to 2.0) |
| presence_penalty | float | No | 0 | Presence penalty (-2.0 to 2.0) |
| seed | int | No | -1 | Random seed (-1 for random) |
| mode | string | No | "instruct" | Chat mode: "instruct", "chat", or "chat-instruct" |
| character | string | No | - | Character name for chat mode |
| instruction_template | string | No | - | Instruction template name |

## Message Format

Each message in the `messages` array should have:

| Field | Type | Description |
|-------|------|-------------|
| role | string | One of: "system", "user", "assistant" |
| content | string | The message content |

### Example with conversation history

```json
{
  "input": {
    "api": {
      "method": "POST",
      "endpoint": "chat/completions"
    },
    "payload": {
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful gardening assistant."
        },
        {
          "role": "user",
          "content": "What's the best time to plant tomatoes?"
        },
        {
          "role": "assistant",
          "content": "The best time to plant tomatoes is after the last frost date in your area, typically in late spring."
        },
        {
          "role": "user",
          "content": "What about in a greenhouse?"
        }
      ],
      "max_tokens": 250
    }
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
    "delayTime": 20275,
    "executionTime": 43997,
    "id": "sync-a3b54383-e671-4e24-a7bd-c5fec16fda3b",
    "output": {
        "id": "chatcmpl-abc123",
        "object": "chat.completion",
        "created": 1703123456,
        "model": "text-generation-webui",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Sure! First you need to dig a hole that is about 1 foot deep by 2 feet wide. Then put some soil into it so there are no air pockets inside of it. Next, place your seedling or sapling into the hole with its roots facing downwards. Finally, cover up the hole with more dirt until only the top few inches of the root ball remain exposed above ground level."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 89,
            "total_tokens": 109
        }
    },
    "status": "COMPLETED"
}
```
