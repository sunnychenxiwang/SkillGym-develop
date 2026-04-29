FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages \
    pytest \
    numpy \
    pandas \
    scikit-learn>=1.0

# Input files
COPY iris.csv /root/

