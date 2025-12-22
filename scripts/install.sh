#!/usr/bin/env bash
set -e

RELEASE="v3.22"
TORCH_VERSION="2.7.1"
PYTHON_VERSION="3.11"
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

echo "Installing Python ${PYTHON_VERSION}"
if [ -n "${PYTHON_VERSION}" ]; then
    # Install Python from deadsnakes PPA
    add-apt-repository ppa:deadsnakes/ppa
    apt install -y --no-install-recommends \
        "python${PYTHON_VERSION}" \
        "python${PYTHON_VERSION}-dev" \
        "python${PYTHON_VERSION}-venv" \
        "python3-tk"

    # Link Python
    rm /usr/bin/python
    ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python
    rm /usr/bin/python3
    ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python3

    # Install pip
    curl -sS https://bootstrap.pypa.io/get-pip.py | python${PYTHON_VERSION}

    # Upgrade pip
    python3 -m pip install --upgrade --no-cache-dir pip

    # Create symlink for pip3
    rm -f /usr/bin/pip3
    ln -s /usr/local/bin/pip3 /usr/bin/pip3
fi

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
mkdir -p /workspace/text-generation-webui/user_data/models
python3 download-model.py ${MODEL} \
  --output /workspace/text-generation-webui/user_data/models

echo "Creating log directory"
mkdir -p /workspace/logs
