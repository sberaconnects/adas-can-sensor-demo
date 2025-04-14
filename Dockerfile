# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy source and config
COPY src/ ./src/
COPY config/ ./config/
COPY requirements.txt ./
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY logs/ ./logs/
COPY README.md ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Optional: Set default command (can override in docker run)
CMD ["python", "src/main.py", "--mode", "replay"]
