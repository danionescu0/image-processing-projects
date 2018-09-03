FROM resin/raspberry-pi-python:3

RUN apt-get update && apt-get install -y git ca-certificates python-opencv


COPY pip.conf /root/.pip/pip.conf
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
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
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*
RUN python3 -m ensurepip --upgrade && pip3 install --upgrade picamera dlib



#FROM generalaardvark/rpi-python35

#RUN pip install --upgrade pip

WORKDIR /root
RUN git clone https://github.com/danionescu0/image-processing-projects.git
COPY ./config.py /root/image-processing-projects/face-recognition-wrapper/config.py
COPY ./requirements.txt /root/image-processing-projects/face-recognition-wrapper/requirements.txt
RUN pip install -qr /root/image-processing-projects/face-recognition-wrapper/requirements.txt

CMD ["python", "/root/image-processing-projects/face-recognition-wrapper/video_processor.py"]
CMD ["python", "/root/image-processing-projects/face-recognition-wrapper/webserver.py"]