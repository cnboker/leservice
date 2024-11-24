sudo apt install docker-buildx
docker buildx create --use --name mybuilder --driver-opt network=host --buildkitd-flags '--allow-insecure-entitlement network.host'

Hi, I spent some time figuring out how to install and use TTS on a Raspberry Pi 3 and 4 (64 bit). Here are the steps:

pip install tts
pip install torch==1.11.0 torchaudio==0.11.0
pip install numpy==1.22.4
sudo apt install llvm-9
LLVM_CONFIG=llvm-config-9 pip install numba==0.51.2
manually download your model and unzip it into $USER/.local/share/tts/
download the .models.json and place it in the app directory

# build docker image
```shell
    sudo docker buildx build --platform linux/arm64 -t gnimi:latest --output type=docker,dest=gnimi_latest.tar .
    scp gnimi_latest.tar voice@192.168.0.102:/home/voice
    docker load -i gnimi_latest.tar

    sudo docker buildx build --platform linux/arm64 -t tts:latest --output type=docker,dest=tts_latest.tar .
    scp tts_latest.tar voice@192.168.0.102:/home/voice
    docker load -i tts_latest.tar
```
