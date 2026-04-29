FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN sed -i 's@http://archive.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g; s@http://security.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g' /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get -o Acquire::Retries=5 -o Acquire::ForceIPv4=true update \
    && apt-get install -y --fix-missing --no-install-recommends python-is-python3 python3 python3-pip ffmpeg ghostscript graphviz imagemagick libreoffice pandoc poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages Pillow defusedxml "markitdown[all]" office pytest

# Input files
COPY Tutorial.docx /root/
COPY sample-word-document.docx /root/
COPY sample.docx /root/
COPY template.docx /root/

