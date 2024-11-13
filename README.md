sudo docker build -t gmini:latest . --network=host --platform linux/arm64
docker save -o gmini.tar gmini:latest
scp gmini.tar voice@192.168.0.102:/home/voice
docker load -i gmini.tar

sudo docker build -t tts:latest . --network=host --platform linux/arm64
docker save -o tts.tar tts:latest
scp tts.tar voice@192.168.0.102:/home/voice
docker load -i tts.tar
