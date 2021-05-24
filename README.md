# RUP

RUP에 탑재되는 model을 훈련하기 위한 repositorie입니다.

[TensorFlow2 Object Detection](https://github.com/tensorflow/models)을 이용하여 object detecion을 수행하였습니다.

TensorFlow2 Object Detection을 수행하기 위한 환경은 Docker를 이용하였고 [docker](https://github.com/hogbal/RUP/tree/master/docker)에서 확인할 수 있습니다.

## 폴더 구조

```sh
├── README.md
├── docker
│   ├── README.md
│   ├── tf-latest
│   │   └── Dockerfile
│   ├── tf2.5.0rc1
│   │   └── Dockerfile
│   ├── tf2.5.0rc2
│   │   └── Dockerfile
│   └── tf2.5.0rc3
│       └── Dockerfile
├── preprocessing
│   ├── change_png_format.ipynb
│   ├── dataset_xml_modify.ipynb
│   ├── modify_dataset.ipynb
│   └── partition_dataset.py
└── tensorflow
    ├── object_detection
    │   └── workspace
    │       └── training_rup
    │           ├── annotations
    │           │   └── label_map.pbtxt
    │           ├── exported-models
    │           │   ├── README.md
    │           │   └── images
    │           │       ├── ssd_mobilenet_v1
    │           │       │   ├── README.md
    │           │       │   ├── image1.png
    │           │       │   ├── image2.png
    │           │       │   ├── image3.png
    │           │       │   ├── image4.png
    │           │       │   ├── image5.png
    │           │       │   ├── image6.png
    │           │       │   └── image7.png
    │           │       ├── ssd_mobilenet_v2
    │           │       │   ├── README.md
    │           │       │   ├── image1.png
    │           │       │   ├── image2.png
    │           │       │   ├── image3.png
    │           │       │   ├── image4.png
    │           │       │   ├── image5.png
    │           │       │   ├── image6.png
    │           │       │   └── image7.png
    │           │       └── ssd_mobilenet_v3
    │           │           ├── README.md
    │           │           ├── image1.png
    │           │           ├── image2.png
    │           │           ├── image3.png
    │           │           ├── image4.png
    │           │           ├── image5.png
    │           │           ├── image6.png
    │           │           └── image7.png
    │           ├── exporter_main_v2.py
    │           ├── mobile
    │           │   └── README.md
    │           ├── model_main_tf2.py
    │           ├── models
    │           │   └── README.md
    │           ├── pre-trained-models
    │           │   └── README.md
    │           ├── predict
    │           │   ├── image1.png
    │           │   ├── image2.png
    │           │   ├── image3.png
    │           │   ├── image4.png
    │           │   ├── image5.png
    │           │   ├── image6.png
    │           │   └── image7.png
    │           └── predict_main_v2.ipynb
    └── script
        ├── generate_tfrecord.py
        └── tensorflow_lite_converter.ipynb
```

[exported-models](https://github.com/hogbal/RUP/tree/master/tensorflow/object_detection/workspace/training_rup/exported-models)에서 학습된 모델을 확인할 수 있습니다.
