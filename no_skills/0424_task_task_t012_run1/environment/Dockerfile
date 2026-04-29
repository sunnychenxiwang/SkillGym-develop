FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages numpy scipy networkx pandas pytest

# Input files
COPY case118.m /root/
COPY case57.m /root/
COPY pglib_opf_case118_ieee.m /root/

