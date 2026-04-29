FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN sed -i 's@http://archive.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g; s@http://security.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g' /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get -o Acquire::Retries=5 -o Acquire::ForceIPv4=true update \
    && apt-get install -y --fix-missing --no-install-recommends python3 python3-pip ghostscript imagemagick \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages fiona geopandas pytest pytest-json-ctrf==0.3.5

# Input files
COPY countries.geo.json /root/
COPY countries.geojson /root/
COPY geo-countries /root/

