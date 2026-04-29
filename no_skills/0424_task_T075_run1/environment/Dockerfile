FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages  numpy pandas scikit-learn==1.4.2 factor-analyzer pytest


# Input files
COPY iris.csv /root/

