#!/usr/bin/env bash

if [ -z "${MODEL+x}" ]; then
  MODEL="TheBloke/Synthia-34B-v1.2-GPTQ"
fi

# Replace slashes with underscores
MODEL="${MODEL//\//_}"
echo "Model: ${MODEL}"

if [ -d "/workspace/text-generation-webui/user_data/models/${MODEL}" ]; then
  echo "Starting Oobabooga Text Generation Server"
  cd /workspace/text-generation-webui
  source /workspace/venv/bin/activate
  mkdir -p /workspace/logs
  nohup python3 server.py \
    --listen \
    --api \
    --loader ExLlamav3 \
    --model ${MODEL} \
    --listen-port 3000 \
    --api-port 5000 \
    --extensions api \
    --trust-remote-code &> /workspace/logs/textgen.log &

  echo "Starting Runpod Handler"
  export PYTHONUNBUFFERED=1
  /workspace/venv/bin/python3 -u /handler.py
else
  echo "Model directory not found!"
fi
