FROM resin/rpi-raspbian:latest

RUN apt-get update && apt-get upgrade && apt-get dist-upgrade

# install build depedencies
RUN apt-get install ca-certificates \
    git \
    wget \
    curl \
    vim \
    python3-pip

RUN apt-get clean
RUN pip3 install --upgrade setuptools

#install project
WORKDIR /root
RUN echo 1 && git clone https://github.com/danionescu0/image-processing-projects.git
COPY ./config.py /root/image-processing-projects/person-monitor/config.py
RUN pip3 install -qr /root/image-processing-projects/person-monitor/requirements.txt

#strip typing from python 3.5 because we're using a python 3.4 version
RUN sed -i "s/from typing import List//g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/from typing import Callable//g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/from typing import Tuple//g" $(find /root/image-processing-projects -type f  -name '*.py')

RUN sed -i "s/Tuple\[int, int\]/tuple/g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/List\[User\]/list/g" $(find /root/image-processing-projects -type f  -name '*.py')
RUN sed -i "s/Callable\[\[codecs.StreamReader\], None\]/object/g" $(find /root/image-processing-projects -type f  -name '*.py')

#run the project
WORKDIR /root/image-processing-projects/person-monitor
#CMD ["python3", "background.py"]
