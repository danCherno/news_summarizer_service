FROM python:3.9.25-alpine3.22
LABEL maintainer="Cherno"

# ============================================
# Python Environment Configuration
# ============================================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

# ============================================
# Working Directory Setup
# ============================================
WORKDIR /app
EXPOSE 8000

# ============================================
# Copy Requirements
# ============================================
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# ============================================
# Build Arguments
# ============================================
ARG DEV=false

# ============================================
# System Dependencies & Python Packages
# ============================================
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # Install PostgreSQL client
    apk add --update --no-cache postgresql-client && \
    # Install temporary build dependencies
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base \
        postgresql-dev \
        musl-dev && \
    # Install production dependencies
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Install development dependencies if DEV=true
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    # Cleanup
    rm -rf /tmp && \
    apk del .tmp-build-deps

# ============================================
# Create Non-Root User
# ============================================
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

# ============================================
# Copy Application Code
# ============================================
COPY ./app /app

# ============================================
# Switch to Non-Root User
# ============================================
USER django-user