FROM tensorflow/tensorflow:2.5.0rc2-gpu

ARG path=/home/hogbal/RUP/object_detection/

RUN apt-get update -y && \
	apt-get upgrade -y && \
	apt-get install python3-dev && \
	apt-get install git -y && \
	apt-get install libgl1-mesa-glx && \
	python3 -m pip install --upgrade pip && \
	pip3 install cython &&\
	apt install protobuf-compiler -y && \
	mkdir /RUP

WORKDIR /RUP


RUN git clone --depth 1 https://github.com/tensorflow/models && \
	git clone https://github.com/cocodataset/cocoapi.git

WORKDIR /RUP/cocoapi/PythonAPI

RUN make && \
	cp -r pycocotools /RUP/models/research

WORKDIR /RUP/models/research

RUN protoc object_detection/protos/*.proto --python_out=. && \
	cp object_detection/packages/tf2/setup.py . && \
	python3 -m pip install .

WORKDIR /RUP/workspace
