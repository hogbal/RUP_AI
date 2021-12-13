FROM nvcr.io/nvidia/tensorrt:21.11-py3

ARG DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH /usr/local/cuda-11.3/compat/:$LD_LIBRARY_PATH

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install build-essential -y && \
	apt-get install python3-dev python3-numpy python3-pip -y && \
	apt-get install tmux -y && \
	apt-get install zsh -y && \
	apt-get install git -y && \
	apt-get install vim -y && \
	apt-get install fonts-powerline -y && \
	apt-get install -y language-pack-en && \
	apt-get install libssl-dev -y && \
	apt install libyaml-cpp-dev curl libeigen3-dev -y && \
	update-locale

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

#setting tkdnn
RUN git clone https://github.com/ceccocats/tkDNN
WORKDIR tkDNN
RUN mkdir build
WORKDIR build
RUN cmake ..
RUN make -j4

WORKDIR /root/tkDNN
RUN git clone https://git.hipert.unimore.it/fgatti/darknet.git
WORKDIR darknet
RUN make -j4
RUN mkdir layers debug

CMD ["zsh"]
