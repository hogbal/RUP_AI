# RUP object detection docker

This is a docker image with Tensorflow 2 object detection API installed.

Pull image from [docker hub](https://hub.docker.com/repository/docker/hogbal/rup)


## docker run
```
docker run --gpus all -it --rm -v [local path]:/RUP/workspace -p 6006:6006 -p 8888:8888 hogbal/rup:2.5.0rc2
```
## Dockerfile table
|Tag|summary|Dockerfile|
|:---:|:---:|:------:|
|2.5.0rc1|using tensorflow/tensorflow:2.5.0rc1-gpu-jupyter image|[2.5.0rc1 Dockerfile](https://github.com/hogbal/RUP/blob/master/docker/tf2.5.0rc1/Dockerfile)|
|2.5.0rc2|using tensorflow/tensorflow:2.5.0rc2-gpu-jupyter image|[2.5.0rc2 Dockerfile](https://github.com/hogbal/RUP/blob/master/docker/tf2.5.0rc2/Dockerfile)|

