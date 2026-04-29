FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN sed -i 's@http://archive.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g; s@http://security.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g' /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get -o Acquire::Retries=5 -o Acquire::ForceIPv4=true update \
    && apt-get install -y --fix-missing --no-install-recommends python3 python3-pip ffmpeg ghostscript imagemagick poppler-utils tesseract-ocr tesseract-ocr-chi-sim python-is-python3\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages Pillow pdf2image pdfplumber pypdf pytest

# Input files
COPY ASD-Cyber-Threat-Report-2024.pdf /root/
COPY RedCanary-Threat-Detection-Report-2024.pdf /root/
COPY Secureworks-State-of-the-Threat-Report-2024.pdf /root/

