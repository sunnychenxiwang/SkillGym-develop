FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN sed -i 's@http://archive.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g; s@http://security.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g' /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get -o Acquire::Retries=5 -o Acquire::ForceIPv4=true update \
    && apt-get install -y --fix-missing --no-install-recommends python3 python3-pip ghostscript imagemagick libreoffice\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Compatibility path for synthesized solutions that read from /root/input
RUN [ -e /root/input ] || ln -s /root /root/input

# Python dependencies
RUN pip3 install --break-system-packages office openpyxl pandas pytest pytest-json-ctrf==0.3.5

# Input files
COPY creditcard.csv /root/
COPY purchases.csv /root/
COPY transactions.csv /root/

