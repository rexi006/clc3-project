FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn azure-eventhub prometheus_client

WORKDIR /app
COPY . /app

EXPOSE 8000

CMD ["python", "main.py"]