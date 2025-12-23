# Step - 1: Builder
FROM python:3.13-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies to /install
COPY requirements.txt . 
# (Make sure to generate requirements.txt from pyproject.toml first!)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Step - 2: Runtime
FROM python:3.13-slim

WORKDIR /app

# Runtime libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . .

# Security
RUN useradd -m appuser
USER appuser

CMD ["python", "src/worker.py"]

COPY . .

# Run the worker script
CMD ["python", "src/worker.py"]