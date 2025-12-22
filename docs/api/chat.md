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
  "delayTime": 101,
  "executionTime": 12359,
  "id": "5d750304-01bd-4d10-8207-a5ce60d1a403-e2",
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "index": 0,
        "message": {
          "content": "Certainly! Planting a tree in your backyard is a rewarding project that can enhance your property's beauty and provide environmental benefits. Here\u2019s a step-by-step guide to help you through the process:\n\n### Step 1: Choose the Right Tree\n1. **Consider the Climate**: Select a tree that is suitable for your local climate.\n2. **Space and Purpose**: Think about the space available and what you want the tree to do. Is it for shade, decoration, or fruit?\n3. **Tree Type**: Choose between deciduous (loses leaves in winter) or evergreen (keeps leaves year-round).\n\n### Step 2: Plan the Location\n1. **Sunlight**: Consider the amount of sunlight the area receives.\n2. **Distance from Structures**: Ensure the tree won\u2019t eventually interfere with your house, power lines, or other structures.\n3. **Soil Conditions**: Check if the soil is well-draining and rich in nutrients.\n\n### Step 3: Prepare the Soil\n1. **Test the Soil**: You can purchase a soil testing kit from a garden center or online.\n2. **Amend the Soil**: Based on the test results, add compost, peat moss, or other amendments to improve soil quality.\n\n### Step 4: Dig the Hole\n1. **Size**: The hole should be about two to three times wider than the root ball of the tree, but no deeper.\n2. **Shape**: The bottom of the hole should be flat, not sloped.\n\n### Step 5: Plant the Tree\n1. **Position the Tree**: Place the tree in the center of the hole, ensuring it is straight.\n2. **Remove Pot or Burlap**: If the tree is in a container, gently remove the pot. For burlap-wrapped trees, remove as much as possible.\n3. **Backfill**: Add soil around the root ball, tamping it down gently to remove air pockets.\n4. **Water**: Water the tree thoroughly to settle the soil around the roots.\n\n### Step 6: Staking (if necessary)\n1. **Support**: If the tree is young or in a windy area, consider staking it. Use stakes and ties that won\u2019t damage the trunk.\n\n### Step 7: Mulching\n1. **Apply Mulch**: Spread a 2-3 inch layer of organic mulch (like bark chips or wood chips) around the base of the tree, keeping it a few inches away from the trunk.\n\n### Step 8: Watering and Maintenance\n1. **Watering**: Water the tree deeply but infrequently to encourage deep root growth.\n2. **Pruning**: Prune any damaged or diseased branches, and remove any suckers that may grow from the base.\n3. **Fertilizing**: Fertilize the tree in early spring and late fall with a balanced fertilizer.\n\n### Step 9: Regular Inspection\n1. **Check for Health**: Regularly inspect the tree for signs of pests or disease.\n2. **Trim as Needed**: Remove dead or diseased branches as needed.\n\nBy following these steps, you can successfully plant a tree in your backyard and enjoy its benefits for years to come.",
          "role": "assistant"
        },
        "tool_calls": []
      }
    ],
    "created": 1766409968,
    "id": "chatcmpl-1766409968820443648",
    "model": "Qwen_Qwen2.5-7B-Instruct",
    "object": "chat.completion",
    "usage": {
      "completion_tokens": 653,
      "prompt_tokens": 47,
      "total_tokens": 700
    }
  },
  "status": "COMPLETED",
  "workerId": "vdu7ciz2x4tm4o"
}
```
