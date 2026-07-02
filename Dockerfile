FROM ubuntu:resolute

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y \
    python3-pip \
    curl \
    openssh-server \
    python3-venv

# Добавляем рабочую директорию для devcontainer
WORKDIR /workspace