FROM nvidia/cuda:11.4.2-cudnn8-devel-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install python3-pip python3-dev build-essential -y && \
	apt-get install libglib2.0-0 -qy && \
	apt-get install libgl1-mesa-glx -y

RUN pip3 install opencv-python && \
	pip3 install requests && \
	pip3 install flask

WORKDIR /server

CMD ["python3","-m","flask","run","--host=0.0.0.0"]
