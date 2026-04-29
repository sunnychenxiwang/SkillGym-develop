FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN sed -i 's@http://archive.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g; s@http://security.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g' /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get -o Acquire::Retries=5 -o Acquire::ForceIPv4=true update \
    && apt-get install -y --fix-missing --no-install-recommends python3 python3-pip ghostscript imagemagick \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages Pillow pdf2image pdfplumber pypdf pytest

# Input files
COPY ASD-Cyber-Threat-Report-2024.pdf /root/input/
COPY RedCanary-Threat-Detection-Report-2024.pdf /root/input/
COPY Secureworks-State-of-the-Threat-Report-2024.pdf /root/input/

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
