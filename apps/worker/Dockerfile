FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# IMPT: Add the virtual environment to the PATH
# This ensures 'python' automatically points to the venv python
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

# Run the worker script
CMD ["python", "src/worker.py"]