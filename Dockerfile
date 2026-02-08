# Dockerfile for OpenWebUI deployment
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv pip install --system open-webui

# Expose port (Railway/Render will set PORT env var, OpenWebUI defaults to 8080)
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data

# Create data directory
RUN mkdir -p /app/data

# Username fix script (run-once on startup; remove after fixing)
COPY fix_username.py /app/fix_username.py
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run fix then OpenWebUI (use PORT env var if provided)
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["sh", "-c", "open-webui serve --host 0.0.0.0 --port ${PORT:-8080}"]
