FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
        libsdl-image1.2-dev \
        libsdl-mixer1.2-dev \
        libsdl-ttf2.0-dev \

        libsdl1.2-dev \

        python3 \
        python3-pip \
        python3-dev \
        python3-setuptools 

COPY . pychess/
WORKDIR /pychess

RUN pip3 install -r requirements.txt

CMD ["./main.py"]
