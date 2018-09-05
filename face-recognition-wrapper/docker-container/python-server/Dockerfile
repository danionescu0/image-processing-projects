FROM generalaardvark/rpi-python35

RUN apt-get update && apt-get install -y git ca-certificates python-opencv

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-pip \
    zip
RUN apt-get clean

RUN pip3 install --upgrade
RUN apt-get install python3-picamera
RUN pip3 install -U pip setuptools

WORKDIR /root
RUN git clone -b 'v19.6' --single-branch https://github.com/davisking/dlib.git 
WORKDIR /root/dlib
RUN python3 setup.py install --compiler-flags "-mfpu=neon"
RUN pip3 install face_recognition


RUN apt-get update \
	&& apt-get install -y --no-install-recommends apt-utils \
	# install necessary libraries \
	&& apt-get -qy install \
		libtiff5-dev \
		libjasper-dev \
		libpng12-dev \
		libv4l-dev \
		libxvidcore-dev \
		libx264-dev \
		libatlas-base-dev \
		python2.7-dev \
		python-pip \
		python-numpy \
		libraspberrypi0 \
		unzip \
	# cleanup apt \
	&& apt-get purge -y --auto-remove \
	&& rm -rf /var/lib/apt/lists/*

ARG OPENCV_VERSION=3.3.1
ENV OPENCV_VERSION $OPENCV_VERSION

	# download latest source & contrib
RUN	cd /tmp \
	&& wget -c -N -nv -O opencv.zip https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip \
	&& unzip opencv.zip \
	&& wget -c -N -nv -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip \
	&& unzip opencv_contrib.zip \
	# build opencv \
	&& cd /tmp/opencv-$OPENCV_VERSION \
	&& mkdir build \
	&& cd build \
	&& cmake -D CMAKE_BUILD_TYPE=RELEASE \
		-D CMAKE_INSTALL_PREFIX=/usr/local \
		-D INSTALL_C_EXAMPLES=ON \
		-D BUILD_PYTHON_SUPPORT=ON \
		-D BUILD_NEW_PYTHON_SUPPORT=ON \
		-D INSTALL_PYTHON_EXAMPLES=ON \
		-D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib-$OPENCV_VERSION/modules \
		-D BUILD_EXAMPLES=ON .. \
	&& make -j4  \
	&& make \
	&& make install\
	# ldconfig && \
	&& make clean \
	# cleanup source \
	&& cd / \
	&& rm -rf /tmp/* \
	&& pip3 install imutils


WORKDIR /root
RUN git clone https://github.com/danionescu0/image-processing-projects.git
COPY ./config.py /root/image-processing-projects/face-recognition-wrapper/config.py
COPY ./requirements.txt /root/image-processing-projects/face-recognition-wrapper/requirements.txt
RUN pip3 install -qr /root/image-processing-projects/face-recognition-wrapper/requirements.txt

CMD ["python3", "/root/image-processing-projects/face-recognition-wrapper/video_processor.py"]
CMD ["python3", "/root/image-processing-projects/face-recognition-wrapper/webserver.py"]
