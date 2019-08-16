FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
        python3 \
        python3-pip \
        python3-dev \
        python3-setuptools 

COPY . pychess/

WORKDIR /pychess

RUN pip3 install -r requirements.txt

CMD ["./main.py"]
