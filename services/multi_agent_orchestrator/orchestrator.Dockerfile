# Multi-Agent Orchestrator Dockerfile
# Optimized for running all 29 agents and meeting system

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire agents directory structure
COPY agents/ ./agents/
COPY Role/ ./Role/
COPY examples/ ./examples/

# Set Python path
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/agents"

# Set environment variables for optimal performance
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_BASE_URL=http://ollama:11434
ENV MODEL_NAME=llama3.2

# Create directory for agent memories and logs
RUN mkdir -p /app/agent_memories /app/logs

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "from agents.orchestrator import AgentOrchestrator; print('OK')" || exit 1

# Default command - run interactive mode
CMD ["python", "-u", "agents/interactive.py"]
