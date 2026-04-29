FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN pip3 install --break-system-packages --no-cache-dir \
    numpy pandas scikit-learn==1.4.2 factor-analyzer pytest


WORKDIR /root

# Python dependencies


# Input files
COPY iris.csv /root/

