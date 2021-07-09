FROM tensorflow/tensorflow:latest-devel-gpu

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install build-essential -y && \
	apt-get install pkg-config -y && \
	apt-get install libjpeg-dev libtiff5-dev libpng-dev -y && \
	apt-get install ffmpeg libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libxine2-dev -y && \
	apt-get install libv4l-dev v4l-utils -y && \
	apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev -y && \
	apt-get install libgtk-3-dev -y && \
	apt-get install mesa-utils libgl1-mesa-dri libgtkgl2.0-dev libgtkglext1-dev -y && \
	apt-get install libatlas-base-dev gfortran libeigen3-dev -y && \
	apt-get install qt5-default -y && \
	apt-get install python3-dev python3-numpy -y && \
	apt-get install git -y && \
	apt-get install wget -y && \
	apt-get install zsh -y && \
	apt-get install tmux -y && \
	apt-get install vim -y && \
	apt install libcanberra-gtk-module libcanberra-gtk3-module -y && \
	apt install libssl-dev -y && \
	apt install fonts-powerline

#setting cuda && cudnn
RUN mv /usr/local/cuda/lib64/libcusolver.so.11 /usr/local/cuda/lib64/libcusolver.so.10

COPY cuda/include/* /usr/local/cuda/include/
COPY cuda/lib64/* /usr/local/cuda/lib64/

RUN chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*

#install cmake
WORKDIR /tf

RUN wget https://cmake.org/files/v3.20/cmake-3.20.4.tar.gz
RUN tar -xvzf cmake-3.20.4.tar.gz && rm cmake-3.20.4.tar.gz

WORKDIR /tf/cmake-3.20.4
RUN ./bootstrap --prefix=/usr/local
RUN make
RUN make install

#install opencv
RUN mkdir /tf/opencv

WORKDIR /tf/opencv

RUN wget -O opencv-4.5.2.zip https://github.com/opencv/opencv/archive/refs/tags/4.5.2.zip
RUN wget -O opencv_contrib-4.5.2.zip https://github.com/opencv/opencv_contrib/archive/4.5.2.zip
RUN unzip opencv-4.5.2.zip
RUN unzip opencv_contrib-4.5.2.zip
RUN rm opencv-4.5.2.zip opencv_contrib-4.5.2.zip

WORKDIR /tf/opencv/opencv-4.5.2

RUN mkdir build

WORKDIR /tf/opencv/opencv-4.5.2/build

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \ 
-D CMAKE_INSTALL_PREFIX=/usr/local \ 
-D WITH_TBB=OFF \
-D WITH_IPP=OFF \
-D WITH_1394=OFF \
-D BUILD_WITH_DEBUG_INFO=OFF \
-D BUILD_DOCS=OFF \
-D INSTALL_C_EXAMPLES=ON \ 
-D INSTALL_PYTHON_EXAMPLES=ON \ 
-D BUILD_EXAMPLES=OFF \
-D BUILD_PACKAGE=OFF \
-D BUILD_TESTS=OFF \
-D BUILD_PERF_TESTS=OFF \ 
-D WITH_QT=OFF \
-D WITH_GTK=ON \
-D WITH_OPENGL=ON \
-D BUILD_opencv_python3=ON \ 
-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.5.2/modules \
-D WITH_V4L=ON \
-D WITH_FFMPEG=ON \ 
-D WITH_XINE=ON \
-D OPENCV_ENABLE_NONFREE=ON \ 
-D BUILD_NEW_PYTHON_SUPPORT=ON \ 
-D OPENCV_SKIP_PYTHON_LOADER=ON \
-D OPENCV_GENERATE_PKGCONFIG=ON ../

RUN make 
RUN make install

#install convert2Yolo
WORKDIR /tf

RUN git clone https://github.com/ssaru/convert2Yolo.git
RUN pip3 install -r convert2Yolo/requirements.txt

#install Yolov4
WORKDIR /tf

RUN git clone https://github.com/AlexeyAB/darknet

WORKDIR darknet

RUN sed -i 's/GPU=0/GPU=1/' ./Makefile && \
	sed -i 's/CUDNN=0/CUDNN=1/' ./Makefile && \
	sed -i 's/OPENCV=0/OPENCV=1/' ./Makefile

RUN mkdir build_release

WORKDIR build_release

RUN cmake ..
RUN cmake --build . --target install --parallel 8

#tensorflow-yolov4-tflite
WORKDIR /tf
RUN git clone https://github.com/hunglc007/tensorflow-yolov4-tflite.git

WORKDIR /tf/tensorflow-yolov4-tflite
RUN pip3 install -r requirements-gpu.txt

#setting vim && tmux
COPY vimrc /root/.vimrc
COPY tmux.conf /root/.tmux.conf

#install oh my zsh
RUN chsh -s /usr/bin/zsh && \
	sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)" && \
	sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/' ~/.zshrc && \
	git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting && \
	git clone https://github.com/zsh-users/zsh-autosuggestions.git ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
	sed -i 's/plugins=(git)/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/' ~/.zshrc

#setting gui
ENV NO_AT_BRIDGE=1
	
COPY cfg/yolov4-obj.cfg /tf/darknet/cfg/yolov4-obj.cfg
COPY data/obj.names /tf/darknet/build/darknet/x64/data/obj.names
COPY data/obj.data /tf/darknet/build/darknet/x64/data/obj.data
COPY data/train.txt /tf/darknet/build/darknet/x64/data/train.txt
COPY data/test.txt /tf/darknet/build/darknet/x64/data/test.txt
COPY pre-trained-weights/yolov4.conv.137 /tf/darknet/build/darknet/x64/yolov4.conv.137

WORKDIR /tf/darknet
CMD ["zsh"]
