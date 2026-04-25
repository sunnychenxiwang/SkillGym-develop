FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip nodejs npm
RUN ln -s /usr/bin/python3 /usr/bin/python
WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages "markitdown[pptx]" pydicom pytest python-pptx

# Input files
COPY CT_small.dcm /root/
COPY MR_small.dcm /root/
COPY rtplan.dcm /root/

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
