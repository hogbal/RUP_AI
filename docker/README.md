# RUP object detection docker

object detection을 하기위한 docker image입니다.

tensorflow는 tensorflow2 object detection API를 이용하였습니다.

docker image는 [docker hub](https://hub.docker.com/repository/docker/hogbal/rup)를 참고하세요.


## docker run
```
docker run --gpus all -it --rm -v [local path]:/RUP/workspace -p 6006:6006 -p 8888:8888 hogbal/rup:[tag]
```
## Dockerfile table
|Tag|summary|Dockerfile|
|:---:|:---:|:------:|
|tf2.5.0rc1|using tensorflow/tensorflow:2.5.0rc1-gpu-jupyter image|[2.5.0rc1 Dockerfile](https://github.com/hogbal/RUP/blob/master/docker/tf2.5.0rc1/Dockerfile)|
|tf2.5.0rc2|using tensorflow/tensorflow:2.5.0rc2-gpu-jupyter image|[2.5.0rc2 Dockerfile](https://github.com/hogbal/RUP/blob/master/docker/tf2.5.0rc2/Dockerfile)|
|tf2.5.0rc3|using tensorflow/tensorflow:2.5.0rc3-gpu-jupyter image|[2.5.0rc3 Dockerfile](https://github.com/hogbal/RUP/blob/master/docker/tf2.5.0rc3/Dockerfile)|
|tf-latest|using tensorflow/tensorflow:latest-gpu-jupyter image|[tf-latest Dockerfile](https://github.com/hogbal/RUP/blob/master/docker/tf-latest/Dockerfile)|
|pytorch|using pytorch/pytorch:lateset image|[pytorch Dockerfile](https://github.com/hogbal/RUP/blob/master/docker/pytorch/Dockerfile)|

