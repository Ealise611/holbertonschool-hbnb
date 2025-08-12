# Dockerfile.app
FROM python:3.9-slim

# Switch working directory
WORKDIR /app

# Install system dependencies for MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 hbnb && chown -R hbnb:hbnb /app
USER hbnb

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# Expose Flask port (Flask runs on 5000 by default)
EXPOSE 5000

# Health check for Flask app
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/api/v1/users/ || exit 1

# Run Flask application
CMD ["python", "run.py"]