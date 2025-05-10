FROM mcr.microsoft.com/devcontainers/python:3.12

# Install system dependencies and pipenv
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    docker.io \
    docker-compose \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv

# Set working directory
WORKDIR /workspace

# Copy Pipenv files early to leverage Docker caching
COPY Pipfile Pipfile.lock ./

# Install both default and dev packages
RUN pipenv install --dev --deploy

# Add environment to PATH (so VS Code uses it)
ENV PIPENV_VENV_IN_PROJECT=1
ENV PATH="/workspace/.venv/bin:$PATH"