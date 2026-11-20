# Image for the window test: Python 3.13 with Tk and a virtual display.
# The test runs on the container's own display, never on the host desktop.
FROM python:3.13-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y xvfb imagemagick x11-utils libtk8.6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app/src:/app
ENV PYTHONDONTWRITEBYTECODE=1

# pypdf reads the sample PDF the window test opens; nothing else is installed.
RUN pip install --no-cache-dir "pypdf~=7.1"
