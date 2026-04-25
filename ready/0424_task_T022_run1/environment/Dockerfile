FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN pip3 install --break-system-packages --no-cache-dir \
    numpy pandas scikit-learn==1.4.2 factor-analyzer pytest


WORKDIR /root

# Python dependencies


# Input files
COPY iris.csv /root/

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
