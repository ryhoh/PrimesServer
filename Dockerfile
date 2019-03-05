FROM python:3.8-rc-alpine3.9
COPY "./src/" "/src/"
WORKDIR "/src/"
CMD ["python", "SocketInterface.py"]