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
RUN python -m venv /py
RUN /py/bin/pip install --upgrade pip
RUN apk add --no-cache postgresql-client jpeg-dev
RUN apk add --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev zlib zlib-dev linux-headers
RUN /py/bin/pip install -r /tmp/requirements.txt
RUN if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi
RUN rm -rf /tmp
RUN apk del .tmp-build-deps
RUN adduser -D -H django-user
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN chown -R django-user:django-user /vol
RUN chmod -R 755 /vol
RUN chmod -R +x /scripts
# Set environment path
ENV PATH="/scripts:/py/bin:$PATH"

# Switch to non-root user for better security
USER django-user

# Default command to run the application
CMD ["run.sh"]