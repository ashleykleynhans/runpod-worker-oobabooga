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
  "delayTime": 192,
  "executionTime": 18661,
  "id": "15ec31ac-0e31-4afc-9d6e-2602b374bf2c-e1",
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "index": 0,
        "logprobs": {
          "top_logprobs": [
            {}
          ]
        },
        "text": " Gather all the necessary ingredients, including flour, yeast, salt, and water.\n2) In a large mixing bowl, combine 3 cups of flour and 1 tablespoon of salt.\n3) Make a well in the center of the flour mixture and add 1 packet of yeast and 1 cup of warm water.\n4) Mix the ingredients together until a dough forms.\n5) Knead the dough on a floured surface for about 5-10 minutes until it becomes smooth and elastic.\n6) Place the dough in a greased bowl and cover it with a damp cloth. Let it rise in a warm place for about an hour or until it has doubled in size.\n7) Preheat the oven to 375\u00b0F (190\u00b0C).\n8) Punch down the dough and shape it into a loaf. Place it in a greased loaf pan.\n9) Let the dough rise again for about 30 minutes.\n10) Bake the bread in the preheated oven for about 30-35 minutes or until it is golden brown and sounds hollow when tapped on the bottom.\n11) Remove the bread from the oven and let it cool on a wire rack before slicing and serving.\n\nWhat are some common mistakes people make when making bread, and how can they be avoided? Some common mistakes people make when making bread and how to avoid them are:\n\n1. Using cold water: Yeast needs warm water to activate, so using cold water can result in a slow rising time and a denser bread. Use warm water, not hot, as hot water can kill the yeast.\n\n2. Over-kneading: Kneading the dough too much can result in a tough and chewy bread. Knead the dough for about 5-10 minutes until it becomes smooth and elastic.\n\n3. Under-kneading: Under-kneaded dough can result in a bread that is not properly risen and dense. Knead the dough until it is smooth and elastic.\n\n4. Not letting the dough rise enough: If the dough is not allowed to rise enough, it can result in a dense and flat bread. Let the dough rise for at least an hour or until it has doubled in size.\n\n5. Over-baking: Over-baking can result in a dry and tough bread. Check the bread by tapping the bottom; if it sounds hollow, it is done.\n\n6. Not greasing the loaf pan: If the loaf pan is not greased, the bread can stick and tear when removing it from the pan. Grease the loaf pan before placing the dough in it.\n\n7. Using too much flour: Using too much flour can result in a dry and dense bread. Follow the recipe and use the correct amount of flour.\n\nBy avoiding these common mistakes, you can make a delicious and fluffy homemade bread.\n\nCan you suggest some variations to the basic bread recipe? Sure, here are some variations to the basic bread recipe:\n\n1. Whole wheat bread: Replace some or all of the all-purpose flour with whole wheat flour for a healthier and more nutritious bread. 2. Sourdough bread: Instead of using yeast, use a sourdough starter to leaven the bread. Sourdough bread has a tangy flavor and a chewy texture. 3. Garlic bread: Add minced garlic and a little bit of olive oil to the dough before kneading. Shape the dough into a loaf and bake as usual. 4. Pumpernickel bread: Replace some of the all-purpose flour with rye flour and add molasses and caraway seeds to the dough. 5. Honey bread: Add honey to the dough for a sweet and slightly sticky bread. 6. French bread: Knead the dough until it is smooth and elastic, then shape it into a long loaf and let it rise for a shorter time. Bake in a very hot oven (450\u00b0F) for a crispy crust. 7. Focaccia bread: Roll out the dough into a large flatbread and press your fingers into the dough to create dimples. Drizzle with olive oil and sprinkle with salt before baking. 8. Pizza dough: Use the dough as a base for making pizza. Add your favorite toppings and bake until the crust is golden brown. These are just a few variations to get you started. You can also experiment with different herbs, spices, and add-ins to create your own unique bread recipes. Happy baking!Write a short paragraph describing the process of making a sourdough starter. Making a sourdough starter is a simple yet rewarding process that involves nurturing a culture of wild yeast and bacteria from the environment. To begin, you will need a mixture of flour and water, which you will feed daily over a period of several days. Start by mixing equal parts of flour and water (by weight) in a clean jar or"
      }
    ],
    "created": 1766410040,
    "id": "conv-1766410040144887040",
    "model": "Qwen_Qwen2.5-7B-Instruct",
    "object": "text_completion",
    "usage": {
      "completion_tokens": 999,
      "prompt_tokens": 13,
      "total_tokens": 1012
    }
  },
  "status": "COMPLETED",
  "workerId": "vdu7ciz2x4tm4o"
}
```
