FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN sed -i 's@http://archive.ubuntu.com/ubuntu@http://mirrors.tuna.tsinghua.edu.cn/ubuntu@g; s@http://security.ubuntu.com/ubuntu@http://mirrors.tuna.tsinghua.edu.cn/ubuntu@g' /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get -o Acquire::Retries=5 -o Acquire::ForceIPv4=true update

RUN apt-get install -y --fix-missing --no-install-recommends \
    python-is-python3 python3 python3-pip ghostscript imagemagick poppler-utils graphviz

RUN apt-get -o Acquire::Retries=10 -o Acquire::ForceIPv4=true -o Acquire::http::Timeout=30 install -y --fix-missing --no-install-recommends pandoc

RUN apt-get -o Acquire::Retries=10 -o Acquire::ForceIPv4=true -o Acquire::http::Timeout=30 install -y --fix-missing --no-install-recommends nodejs npm

RUN apt-get install -y --fix-missing --no-install-recommends \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages Pillow defusedxml mammoth markitdown python-docx office pytest
RUN npm install -g --force mammoth

# Input files
COPY Tutorial.docx /root/input/
COPY sample-word-document.docx /root/input/
COPY sample.docx /root/input/
COPY template.docx /root/input/

# Copy skills to agent-specific locations
# Claude Code
COPY skills /root/.claude/skills
# Codex
COPY skills /root/.codex/skills
# OpenCode - singular "skill"
COPY skills /root/.opencode/skill
# Goose
COPY skills /root/.goose/skills
# Factory
COPY skills /root/.factory/skills
# Portable agents format (Goose, Amp)
COPY skills /root/.agents/skills
# Gemini
COPY skills /root/.gemini/skills
