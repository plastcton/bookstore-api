FROM ubuntu:resolute

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install --no-install-recommends -y \
        curl \
        openssh-server \
        python3-pip \
        python3-venv 