FROM ubuntu:latest
RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install python3 git
WORKDIR /home/has
COPY requirements.txt .
RUN pip install -r requirements.txt