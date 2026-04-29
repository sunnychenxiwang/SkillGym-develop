FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 
RUN pip3 install --break-system-packages polars numpy scikit-learn matplotlib openpyxl
WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages polars

# Input files
COPY iris.csv /root/

