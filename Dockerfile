# Use Python 3.9 with Alpine Linux 3.13 as the base image
FROM python:3.9-alpine3.13

# Prevent Python from buffering outputs
ENV PYTHONUNBUFFERED 1

# Set up working directory and copy necessary files
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app

WORKDIR /app
EXPOSE 8000

# Argument to determine if it's a development build
ARG DEV=false

# Install system dependencies and Python packages
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --no-cache \
    postgresql-client \
    jpeg-dev && \
    apk add --no-cache --virtual .tmp-build-deps \
    build-base \
    postgresql-dev \
    musl-dev \
    zlib \
    zlib-dev \
    linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
    /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser -D -H django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

# Set environment path
ENV PATH="/scripts:/py/bin:$PATH"

# Switch to non-root user for better security
USER django-user

# Default command to run the application
CMD ["run.sh"]