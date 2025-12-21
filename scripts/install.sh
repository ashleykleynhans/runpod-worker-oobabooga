#!/usr/bin/env bash
set -e

RELEASE="v3.22"
TORCH_VERSION="2.7.1"
MODEL="TheBloke/Synthia-34B-v1.2-GPTQ"

echo "Deleting Oobabooga Text Generation Web UI"
rm -rf /workspace/text-generation-webui

echo "Deleting venv"
rm -rf /workspace/venv

echo "Cloning Oobabooga Text Generation Web UI repo to /workspace"
cd /workspace
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
git checkout ${RELEASE}

echo "Installing Ubuntu updates"
apt update
apt -y upgrade

echo "Creating and activating venv"
cd /workspace/text-generation-webui
python3 -m venv /workspace/venv
source /workspace/venv/bin/activate

echo "Installing Torch"
pip3 install --no-cache-dir torch==${TORCH_VERSION} torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

echo "Installing Oobabooga Text Generation Web UI"
pip3 install -r requirements/full/requirements.txt
bash -c 'for req in extensions/*/requirements.txt ; do pip3 install -r "$req" ; done'

echo "Fixing numpy and pandas incompatibility issue"
pip3 install --force-reinstall numpy==2.2.* pandas

echo "Installing RunPod Serverless dependencies"
cd /workspace/text-generation-webui
pip3 install huggingface_hub runpod==1.7.10

echo "Downloading model: ${MODEL}"
cd /workspace/text-generation-webui
python3 download-model.py ${MODEL} \
  --output /workspace/text-generation-webui/models

echo "Creating log directory"
mkdir -p /workspace/logs
