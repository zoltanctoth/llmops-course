FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Add Docker configuration to ignore secrets warnings
RUN mkdir -p /home/vscode/.docker && \
    echo '{"warnings": {"SecretsUsedInArgOrEnv": "ignore"}}' > /home/vscode/.docker/config.json && \
    chown -R vscode:vscode /home/vscode/.docker

# Update apt and install system dependencies
RUN apt-get update && \
    apt-get install -y shellcheck && \
    # Install dependencies for pyenv and Python building
    apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git curl && \
    # Install Node.js 20.x
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    # Install devcontainer CLI globally
    npm install -g @devcontainers/cli

ENV PATH=/home/vscode/.local/bin:$PATH

# Install pyenv
RUN curl https://pyenv.run | bash && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc && \
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc && \
    echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc

RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

USER vscode

COPY requirements.txt /tmp/requirements.txt
RUN pip install --user -r /tmp/requirements.txt


EXPOSE 5050
EXPOSE 8050
