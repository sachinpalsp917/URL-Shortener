#Use official lightweight Python image
FROM python:3.13-slim

# Install uv by copying the binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency definition files first (for Docker layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen: strict locking (don't update lockfile)
# --no-dev: do not install dev dependecies
RUN uv sync --frozen --no-dev

# Copy the application code
COPY . .

# Expose port
EXPOSE 8000


# Run the application
# uv run automatically uses the virtual environment created by uv sync
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
