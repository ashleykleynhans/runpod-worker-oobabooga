## Building the Worker with a Network Volume

This will store your application on a Runpod Network Volume and
build a light weight Docker image that runs everything
from the Network volume without installing the application
inside the Docker image.

1. [Create a Runpod Account](https://runpod.io?ref=2xxro4sy).
2. Create a [Runpod Network Volume](https://www.runpod.io/console/user/storage). You'll need about 15GB of space, plus space for your model(s).
3. Attach the Network Volume to a Secure Cloud [GPU pod](https://www.runpod.io/console/gpu-secure-cloud).
4. Select the Runpod Pytorch 2.4.0 Template.
5. Deploy the GPU Cloud pod.
6. Once the pod is up, open a Terminal and install the required
   dependencies. This can either be done by using the installation
   script, or manually.

## Automatic Installation Script

You can run this automatic installation script which will
automatically install all of the dependencies that get installed
manually below, and then you don't need to follow any of the
manual instructions.

```bash
wget https://raw.githubusercontent.com/ashleykleynhans/runpod-worker-oobabooga/main/scripts/install.sh
chmod +x install.sh
./install.sh
```

## Manual Installation

### Install Python 3.13

The Runpod Pytorch template ships with Python 3.11, but Python 3.13 is required.

```bash
add-apt-repository ppa:deadsnakes/ppa
apt install -y python3.13 python3.13-dev python3.13-venv
rm -f /usr/bin/python /usr/bin/python3
ln -s /usr/bin/python3.13 /usr/bin/python
ln -s /usr/bin/python3.13 /usr/bin/python3
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13
```

### Install oobabooga text-generation-webui

```bash
cd /workspace
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
git checkout v4.1.1
python3 -m venv /workspace/venv
source /workspace/venv/bin/activate
pip3 install --no-cache-dir torch==2.9.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
pip3 install -r requirements/full/requirements.txt
bash -c 'for req in extensions/*/requirements.txt ; do pip3 install -r "$req" ; done'
pip3 install --force-reinstall numpy==2.2.* pandas
```
7. Install the Serverless dependencies:
```bash
pip3 install huggingface_hub runpod==1.7.10
```
8. Download a model, for example `Qwen/Qwen2.5-7B-Instruct`:
```bash
wget https://raw.githubusercontent.com/ashleykleynhans/runpod-worker-oobabooga/refs/heads/main/download_model.py -O /download_model.py
chmod +x /download_model.py
wget https://raw.githubusercontent.com/ashleykleynhans/runpod-worker-oobabooga/refs/heads/main/fetch_model.py
mkdir -p /workspace/text-generation-webui/user_data/models
python3 fetch_model.py ${MODEL} /workspace/text-generation-webui/user_data/models
```
9. Everything should now be installed on your Network Volume and it
   should be safe to terminate the pod.
10. Sign up for a Docker hub account if you don't already have one.
11. Build the Docker image on your local machine and push to Docker hub:
```bash
docker buildx bake network-volume
docker login
docker push dockerhub-username/runpod-worker-oobabooga:4.0.0-network-volume
```
