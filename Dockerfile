# Base image for router
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY setup.py .
COPY src/ ./src/

# Create non-root user and set permissions
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Set environment variables and expose port
ENV PYTHONUNBUFFERED=1
ENV PORT=3000
EXPOSE ${PORT}

# Run the router
CMD ["python", "-m", "src.run_router"]