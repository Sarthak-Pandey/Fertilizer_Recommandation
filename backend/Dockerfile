FROM python:3.13.1-slim

WORKDIR /app

# Create dedicated non-root application user
RUN useradd -m -u 1000 appuser

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Set ownership to appuser
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Docker Healthcheck targeting backend health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
