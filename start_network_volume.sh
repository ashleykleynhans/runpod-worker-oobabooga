#!/usr/bin/env bash

# Set default model if its not set in the environment variable
if [ -z "${MODEL+x}" ]; then
  MODEL="TheBloke/Synthia-34B-v1.2-GPTQ"
fi

# Replace slashes with underscores
MODEL="${MODEL//\//_}"
echo "Model: ${MODEL}"

if [[ ! -L /workspace ]]; then
  echo "Symlinking files from Network Volume"
  ln -s /runpod-volume /workspace
fi

if [ -d "/runpod-volume/text-generation-webui/models/${MODEL}" ]; then
  echo "Starting Oobabooga Text Generation Server"
  cd /runpod-volume/text-generation-webui
  source /workspace/venv/bin/activate
  mkdir -p /runpod-volume/logs
  nohup python3 server.py \
    --listen \
    --api \
    --model ${MODEL} \
    --loader ExLlamav3 \
    --listen-port 3000 \
    --api-port 5000 \
    --extensions api \
    --trust-remote-code &> /runpod-volume/logs/textgen.log &

  echo "Starting Runpod Handler"
  export PYTHONUNBUFFERED=1
  python3 -u /handler.py
else
  echo "Model directory not found!"
fi
