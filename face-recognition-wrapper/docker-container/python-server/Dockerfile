FROM resin/rpi-raspbian:latest

RUN apt-get update
RUN apt-get upgrade

# install build depedencies
RUN apt-get install build-essential \
    ca-certificates \
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
    libgtk-3-dev \
    zip \
    libtiff5-dev \
    libjasper-dev \
    libpng12-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libatlas-base-dev \
    libraspberrypi0 \
    unzip

RUN apt-get clean
RUN pip3 install numpy

WORKDIR opencv
RUN wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.0.zip
RUN unzip opencv.zip
RUN wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.3.0.zip
RUN unzip opencv_contrib.zip


WORKDIR opencv-3.3.0
RUN mkdir build
WORKDIR build
RUN  cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv/opencv_contrib-3.3.0/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

RUN apt-get install -y dphys-swapfile
# Just in case the default is too small adjust it size
RUN sed -i 's/CONF_SWAPSIZE=100$/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile
RUN /etc/init.d/dphys-swapfile stop
RUN /etc/init.d/dphys-swapfile start

RUN make -j3
RUN make install
RUN ldconfig
# Clean up and reduce the image size by deleting files
WORKDIR /
RUN rm -rf /opencv

RUN pip3 install --upgrade setuptools

#install dlib and face_recognition library
WORKDIR /root
RUN git clone -b 'v19.6' --single-branch https://github.com/davisking/dlib.git
WORKDIR /root/dlib
RUN python3 setup.py install --compiler-flags "-mfpu=neon"
RUN pip3 install face_recognition

RUN pip3 install picamera

#install project
WORKDIR /root
RUN echo 5 && git clone https://github.com/danionescu0/image-processing-projects.git
COPY ./config.py /root/image-processing-projects/face-recognition-wrapper/config.py
COPY ./requirements.txt /root/image-processing-projects/face-recognition-wrapper/requirements.txt
RUN pip3 install -qr /root/image-processing-projects/face-recognition-wrapper/requirements.txt

#strip typing from python 3.5 because we're using a python 3.4 version
RUN sed -i "s/from typing import List//g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/from typing import Callable//g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/from typing import Optional//g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/List\[DetectedFace\]/list/g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/Callable\[\[codecs.StreamReader\], None\]/object/g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/Optional\[User\]/object/g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/List\[str\]/list/g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/List\[User\]/list/g" $(find /root/image-processing-projects -type f  -name '*.py')

#run the project
WORKDIR /root/image-processing-projects/face-recognition-wrapper
CMD ["python3", "webserver.py"]
CMD ["python3", "video_processor.py", "--camera_device", "0"]

EXPOSE 8080