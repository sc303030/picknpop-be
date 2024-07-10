FROM python:3.12-slim
WORKDIR /
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY ./app /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
