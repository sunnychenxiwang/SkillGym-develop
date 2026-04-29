FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages  numpy pandas statsmodels aeon pytest

# Input files
COPY datagetter /root/
COPY datagetter_2 /root/
COPY datagetter_3 /root/
COPY datagetter_5 /root/

