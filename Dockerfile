FROM ubuntu:latest
RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install python3 python3-pip ansible
WORKDIR /home/has
COPY ./* .
RUN pip install -r requirements.txt
ENTRYPOINT python /home/has/has_controller.py
