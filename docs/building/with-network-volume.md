## Building the Worker with a Network Volume

This will store your application on a Runpod Network Volume and
build a light weight Docker image that runs everything
from the Network volume without installing the application
inside the Docker image.

1. [Create a RunPod Account](https://runpod.io?ref=2xxro4sy).
2. Create a [RunPod Network Volume](https://www.runpod.io/console/user/storage). You'll need about 15GB of space, plus space for your model(s).
3. Attach the Network Volume to a Secure Cloud [GPU pod](https://www.runpod.io/console/gpu-secure-cloud).
4. Select the RunPod Pytorch 2.1 Template.
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

```bash
cd /workspace
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
git checkout 2af7e382b121f2eae16dd1f7ace621d31028b319
python3 -m venv /workspace/venv
source /workspace/venv/bin/activate
pip3 install --no-cache-dir torch==2.1.2 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip3 install --no-cache-dir xformers
pip3 install -r requirements.txt
bash -c 'for req in extensions/*/requirements.txt ; do pip3 install -r "$req" ; done'
mkdir -p repositories
cd repositories
git clone https://github.com/turboderp/exllama
pip3 install -r exllama/requirements.txt
```
7. Install the Serverless dependencies:
```bash
pip3 install huggingface_hub runpod
```
8. Download a model, for example `TheBloke/Synthia-34B-v1.2-GPTQ`:
```bash
cd /workspace/text-generation-webui
python3 download-model.py TheBloke/Synthia-34B-v1.2-GPTQ \
  --output /workspace/text-generation-webui/models
```
## Final steps
1. Everything should now be installed on your Network Volume and it
   should be safe to terminate the pod.
2. Sign up for a Docker hub account if you don't already have one.
3. Build the Docker image on your local machine and push to Docker hub:
```bash
docker build -t dockerhub-username/runpod-worker-oobabooga:latest -f Dockerfile.Network_Volume .
docker login
docker push dockerhub-username/runpod-worker-oobabooga:latest
```
