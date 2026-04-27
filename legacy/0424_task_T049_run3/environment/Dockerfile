FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y \
      python3 python3-pip \
      build-essential \
      python3-dev \
      && rm -rf /var/lib/apt/lists/*


WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages pandas numpy scikit-learn==1.2.2 factor-analyzer pytest

# Input files
COPY airlines.csv /root/
COPY flights_2.csv /root/

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
