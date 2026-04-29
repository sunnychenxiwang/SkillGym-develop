FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages pandas openpyxl pytest numpy scipy

# Input files
COPY Dataset_S9.csv /root/
COPY construction.csv /root/
COPY construction_spending.csv /root/

