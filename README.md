sudo docker build -t gmini:latest . --network=host
DOCKER_BUILDKIT=1 docker build -f services/ttservice/Dockerfile --build-context root=./ -t ttsservice:latest .
