## Deep Learning

- [Darknet](https://github.com/AlexeyAB/darknet) 프레임워크를 이용해서 일회용 플라스틱 컵의 재질을 식별하기 위한 Object Detection 모델을 학습했습니다.
- Jetson nano라는 임베디드 장치에 탑재하기 위해 속도와 정확도를 고려해서 YOLOv7-tiny 모델을 사용해 학습을 진행했습니다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/34f5b616-6677-4cb9-b6da-0f12d3478e0a/e689b62b-3edc-4936-83c8-625172296326/Untitled.png)

## jetson nano

![jetson nano 이미지](https://prod-files-secure.s3.us-west-2.amazonaws.com/34f5b616-6677-4cb9-b6da-0f12d3478e0a/c9973818-92cf-4a64-9f0f-8a68ec8908a4/Untitled.png)

jetson nano 이미지

- jetson nano는 NVIDIA에서 개발한 임베디드 장치로, GPU를 탑재해서 end-ponit에서 Deep Learning 모델이 작동하도록 설계된 장치입니다.
- 학습된 YOLOv7 모델이 해당 장치에서 작동할 수 있도록 python 코드를 이용해서 개발하였습니다.
