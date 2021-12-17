FROM nvidia/cuda:11.4.2-cudnn8-devel-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

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
	apt-get install python3-dev python3-numpy python3-pip -y && \
	apt-get install git -y && \
	apt-get install wget -y && \
	apt-get install zsh -y && \
	apt-get install tmux -y && \
	apt-get install vim -y && \
	apt-get install -y language-pack-en && \
	apt-get install libglib2.0-0 -qy && \
	apt-get install libgl1-mesa-glx -y && \
	apt install libcanberra-gtk-module libcanberra-gtk3-module -y && \
	apt install libssl-dev -y && \
	apt install fonts-powerline -y && \
	apt install zip -y

RUN pip3 install opencv-python && \
	pip3 install requests && \
	pip3 install flask && \
	pip3 install natsort

#install cmake
WORKDIR /root

RUN wget https://cmake.org/files/v3.20/cmake-3.20.4.tar.gz
RUN tar -xvzf cmake-3.20.4.tar.gz && rm cmake-3.20.4.tar.gz

WORKDIR /root/cmake-3.20.4
RUN ./bootstrap --prefix=/usr/local
RUN make -j4
RUN make install

#install opencv
RUN mkdir /root/opencv

WORKDIR /root/opencv

RUN wget -O opencv-4.5.2.zip https://github.com/opencv/opencv/archive/refs/tags/4.5.2.zip
RUN wget -O opencv_contrib-4.5.2.zip https://github.com/opencv/opencv_contrib/archive/4.5.2.zip
RUN unzip opencv-4.5.2.zip
RUN unzip opencv_contrib-4.5.2.zip
RUN rm opencv-4.5.2.zip opencv_contrib-4.5.2.zip

WORKDIR /root/opencv/opencv-4.5.2

RUN mkdir build

WORKDIR /root/opencv/opencv-4.5.2/build

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

RUN make -j4
RUN make install

#setting vim
COPY vimrc /root/.vimrc

#setting tmux
WORKDIR /root
RUN git clone https://github.com/gpakosz/.tmux.git
RUN ln -s -f .tmux/.tmux.conf
RUN cp .tmux/.tmux.conf.local .

#install oh my zsh
RUN chsh -s /usr/bin/zsh && \
	sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)" && \
	sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/' ~/.zshrc && \
	git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting && \
	git clone https://github.com/zsh-users/zsh-autosuggestions.git ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
	sed -i 's/plugins=(git)/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/' ~/.zshrc

#setting gui
ENV NO_AT_BRIDGE=1

WORKDIR /server
