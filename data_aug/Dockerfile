FROM nvcr.io/nvidia/tensorrt:21.11-py3

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install python3-pip python3-dev build-essential -y && \
	apt-get install libglib2.0-0 -qy && \
	apt-get install libgl1-mesa-glx -y && \
	pip3 install opencv-python

COPY . /server
