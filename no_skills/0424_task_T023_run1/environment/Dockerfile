FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages biopython pytest numpy

# Input files
COPY SRR020192.fastq.gz /root/
COPY example.fastq /root/

