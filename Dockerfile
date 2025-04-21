FROM python:3.12.0-bullseye

# Force stdin, stdout, and stderr to be totally unbuffered
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.6.1
ARG DEBIAN_FRONTEND=noninteractive

# Retry and timeout settings for slow mirrors
RUN echo 'Acquire::Retries "5";\nAcquire::http::Timeout "60";' > /etc/apt/apt.conf.d/80retries

# Core system packages
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        libcurl4-openssl-dev \
        wget \
        gnupg \
        lsb-release \
        locales \
        curl \
        acl \
        ca-certificates; \
    sed -i 's/^# *\(en_US\.UTF-8\)/\1/' /etc/locale.gen; \
    locale-gen; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

# Python tooling
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Set working directory
WORKDIR /app

# Set default permissions for mounted directories
RUN setfacl -d -m u::rwx,g::rwx,o::rwx /app

COPY pyproject.toml ./

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

CMD ["/bin/bash"]
