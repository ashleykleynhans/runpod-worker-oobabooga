## Building the Worker without a Network Volume

This is the simpler option.  No network volume is required.
The entire application will be stored within the Docker image
but will obviously create a more bulky Docker image as a result.

```bash
docker build -t dockerhub-username/runpod-worker-oobabooga:1.0.0 -f Dockerfile.Standalone .
docker login
docker push dockerhub-username/runpod-worker-oobabooga:1.0.0
```
