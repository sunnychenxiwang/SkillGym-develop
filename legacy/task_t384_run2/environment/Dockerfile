FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN sed -i 's@http://archive.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g; s@http://security.ubuntu.com/ubuntu@http://mirrors.ustc.edu.cn/ubuntu@g' /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get -o Acquire::Retries=5 -o Acquire::ForceIPv4=true update \
    && apt-get install -y --fix-missing --no-install-recommends python3 python3-pip ghostscript imagemagick libreoffice poppler-utils file unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages Pillow defusedxml office openpyxl==3.0.10 pandas==2.1.4 pytest

# Test compatibility: expose coordinate_from_string at openpyxl.utils level.
RUN python3 -c "from pathlib import Path; p=Path('/usr/local/lib/python3.12/dist-packages/openpyxl/utils/__init__.py'); t=p.read_text(encoding='utf-8'); s='from .cell import coordinate_from_string\\n'; p.write_text((s+t) if 'coordinate_from_string' not in t else t, encoding='utf-8')"

# Input files
COPY ["Dataset S9.csv", "/root/"]
COPY construction.csv /root/
COPY construction_spending.csv /root/

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
