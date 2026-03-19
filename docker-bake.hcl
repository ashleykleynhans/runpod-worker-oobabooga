variable "REGISTRY" {
    default = "docker.io"
}

variable "REGISTRY_USER" {
    default = "ashleykza"
}

variable "APP" {
    default = "runpod-worker-oobabooga"
}

variable "RELEASE" {
    default = "4.0.0"
}

variable "CUDA_VERSION" {
    default = "12.8.1"
}

variable "PYTHON_VERSION" {
    default = "3.13"
}

variable "OOBABOOGA_RELEASE" {
    default = "v4.1.1"
}

variable "TORCH_VERSION" {
    default = "2.9.1"
}

variable "MODEL" {
    default = "Qwen/Qwen2.5-7B-Instruct"
}

group "default" {
    targets = ["standalone", "network-volume"]
}

target "standalone" {
    dockerfile = "Dockerfile.Standalone"
    tags = ["${REGISTRY}/${REGISTRY_USER}/${APP}:${RELEASE}-standalone"]
    args = {
        CUDA_VERSION = "${CUDA_VERSION}"
        PYTHON_VERSION = "${PYTHON_VERSION}"
        OOBABOOGA_RELEASE = "${OOBABOOGA_RELEASE}"
        TORCH_VERSION = "${TORCH_VERSION}"
        MODEL = "${MODEL}"
    }
}

target "network-volume" {
    dockerfile = "Dockerfile.Network_Volume"
    tags = ["${REGISTRY}/${REGISTRY_USER}/${APP}:${RELEASE}-network-volume"]
    args = {
        CUDA_VERSION = "${CUDA_VERSION}"
        PYTHON_VERSION = "${PYTHON_VERSION}"
    }
}
