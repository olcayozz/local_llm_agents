# Deployment and Setup Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Deployment Options](#deployment-options)
5. [Production Setup](#production-setup)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)

---

## Prerequisites

### System Requirements

#### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS (10.15+), Windows 10/11
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Storage**: 20 GB free space
- **Python**: 3.8 or higher

#### Recommended Requirements
- **OS**: Linux (Ubuntu 22.04+)
- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Storage**: 50+ GB SSD
- **Python**: 3.10 or higher
- **GPU**: NVIDIA GPU with 8GB+ VRAM (optional, for faster inference)

### Software Dependencies

- **Ollama**: Local LLM runtime
- **Python 3.8+**: Programming language
- **pip**: Python package manager
- **Git**: Version control (optional)

---

## Installation

### Step 1: Install Ollama

#### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS

```bash
brew install ollama
```

#### Windows

Download and install from [https://ollama.ai/download](https://ollama.ai/download)

### Step 2: Pull LLM Models

```bash
# Pull default model
ollama pull llama3.2

# Optional: Pull additional models
ollama pull mistral
ollama pull codellama
ollama pull llama2
```

### Step 3: Verify Ollama Installation

```bash
# Check Ollama is running
ollama list

# Test model
ollama run llama3.2 "Hello, how are you?"
```

### Step 4: Clone Repository

```bash
git clone https://github.com/yourusername/local_llm_agents.git
cd local_llm_agents
```

### Step 5: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Step 6: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 7: Verify Installation

```bash
# Run test script
python tests/test_all_agents.py

# Expected output: All 29 agents initialized successfully
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_TIMEOUT=300

# Model Configuration
DEFAULT_MODEL=llama3.2
DEFAULT_TEMPERATURE=0.7

# Role Configuration
ROLE_FOLDER=Role

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/agent_system.log

# Performance
MAX_WORKERS=10
ENABLE_CACHING=true
CACHE_TTL=3600
```

### Configuration File

Create `config.yaml`:

```yaml
orchestrator:
  model_name: "llama3.2"
  temperature: 0.7
  role_folder: "Role"
  max_memory_messages: 100

ollama:
  host: "http://localhost:11434"
  timeout: 300
  retry_attempts: 3
  retry_delay: 5

agents:
  backend_developer:
    model: "llama3.2"
    temperature: 0.7
  security_engineer:
    model: "llama3.2"
    temperature: 0.5
  # ... configure other agents

meetings:
  max_duration_minutes: 120
  auto_save: true
  save_path: "meetings/"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/agent_system.log"
  max_bytes: 10485760  # 10MB
  backup_count: 5

performance:
  enable_parallel_execution: true
  max_workers: 10
  enable_caching: true
  cache_ttl: 3600
```

### Role Files

Ensure all role files are in the `Role/` directory:

```bash
ls -la Role/

# Expected output:
# Software_Developer_Backend.txt
# Software_Developer_Frontend.txt
# ... (29 role files total)
```

---

## Deployment Options

### Option 1: Local Development

Best for: Development, testing, small-scale usage

```bash
# Start Ollama service
ollama serve

# In another terminal, run your application
python examples/meeting_examples.py
```

### Option 2: Docker Deployment

Best for: Consistent environments, easy deployment

#### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose ports
EXPOSE 8000

# Start script
CMD ["python", "main.py"]
```

#### Create docker-compose.yml

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

  agent_system:
    build: .
    depends_on:
      - ollama
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - DEFAULT_MODEL=llama3.2
    volumes:
      - ./Role:/app/Role
      - ./logs:/app/logs
      - ./meetings:/app/meetings
    ports:
      - "8000:8000"
    restart: unless-stopped

volumes:
  ollama_data:
```

#### Deploy with Docker

```bash
# Build and start services
docker-compose up -d

# Pull models
docker-compose exec ollama ollama pull llama3.2

# View logs
docker-compose logs -f agent_system

# Stop services
docker-compose down
```

### Option 3: Kubernetes Deployment

Best for: Production, high availability, scalability

#### Create Kubernetes manifests

**ollama-deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        ports:
        - containerPort: 11434
        volumeMounts:
        - name: ollama-data
          mountPath: /root/.ollama
      volumes:
      - name: ollama-data
        persistentVolumeClaim:
          claimName: ollama-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: ollama
spec:
  selector:
    app: ollama
  ports:
  - port: 11434
    targetPort: 11434
```

**agent-system-deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-system
  template:
    metadata:
      labels:
        app: agent-system
    spec:
      containers:
      - name: agent-system
        image: your-registry/agent-system:latest
        env:
        - name: OLLAMA_HOST
          value: "http://ollama:11434"
        - name: DEFAULT_MODEL
          value: "llama3.2"
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: role-files
          mountPath: /app/Role
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: role-files
        configMap:
          name: role-files
      - name: logs
        persistentVolumeClaim:
          claimName: logs-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: agent-system
spec:
  type: LoadBalancer
  selector:
    app: agent-system
  ports:
  - port: 80
    targetPort: 8000
```

#### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace agent-system

# Apply manifests
kubectl apply -f ollama-deployment.yaml -n agent-system
kubectl apply -f agent-system-deployment.yaml -n agent-system

# Check status
kubectl get pods -n agent-system

# View logs
kubectl logs -f deployment/agent-system -n agent-system
```

### Option 4: Cloud Deployment

#### AWS EC2

```bash
# Launch EC2 instance (Ubuntu 22.04, t3.xlarge or larger)
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install -y python3-pip git

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Clone and setup
git clone https://github.com/yourusername/local_llm_agents.git
cd local_llm_agents
pip3 install -r requirements.txt

# Pull models
ollama pull llama3.2

# Run application
python3 main.py
```

#### Google Cloud Platform

```bash
# Create VM instance
gcloud compute instances create agent-system \
  --machine-type=n1-standard-4 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB

# SSH and setup (same as AWS)
```

#### Azure

```bash
# Create VM
az vm create \
  --resource-group agent-system-rg \
  --name agent-system-vm \
  --image UbuntuLTS \
  --size Standard_D4s_v3 \
  --admin-username azureuser

# SSH and setup (same as AWS)
```

---

## Production Setup

### 1. Security Hardening

#### Enable HTTPS

```python
# Use reverse proxy (nginx)
# /etc/nginx/sites-available/agent-system

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Implement Authentication

```python
# Add authentication middleware
from functools import wraps
from flask import request, abort

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_KEY'):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function
```

#### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route("/agent/chat")
@limiter.limit("10 per minute")
def chat():
    # ... implementation
```

### 2. Performance Optimization

#### Enable Caching

```python
from functools import lru_cache
import redis

# Redis cache
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_response(key, value, ttl=3600):
    redis_client.setex(key, ttl, value)

def get_cached_response(key):
    return redis_client.get(key)
```

#### Connection Pooling

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)

def parallel_agent_execution(agents, query):
    futures = [executor.submit(agent.chat, query) for agent in agents]
    return [f.result() for f in futures]
```

### 3. Monitoring Setup

#### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
request_count = Counter('agent_requests_total', 'Total agent requests')
request_duration = Histogram('agent_request_duration_seconds', 'Request duration')

@request_duration.time()
def process_request():
    request_count.inc()
    # ... process request
```

#### Health Checks

```python
@app.route("/health")
def health_check():
    return {
        "status": "healthy",
        "ollama": check_ollama_connection(),
        "agents": len(orchestrator.list_agents()),
        "timestamp": datetime.now().isoformat()
    }
```

### 4. Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler(
    'logs/agent_system.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

handler.setFormatter(formatter)
logger = logging.getLogger('agent_system')
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

### 5. Backup Strategy

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/agent_system"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup role files
tar -czf "$BACKUP_DIR/roles_$DATE.tar.gz" Role/

# Backup meetings
tar -czf "$BACKUP_DIR/meetings_$DATE.tar.gz" meetings/

# Backup logs
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" logs/

# Backup configuration
cp config.yaml "$BACKUP_DIR/config_$DATE.yaml"

# Remove old backups (keep last 30 days)
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
```

---

## Monitoring

### Metrics to Monitor

1. **System Metrics**
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network I/O

2. **Application Metrics**
   - Request rate
   - Response time
   - Error rate
   - Agent usage

3. **LLM Metrics**
   - Inference time
   - Token usage
   - Model availability

### Monitoring Tools

#### Grafana Dashboard

```yaml
# grafana-dashboard.json
{
  "dashboard": {
    "title": "Agent System Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(agent_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, agent_request_duration_seconds)"
          }
        ]
      }
    ]
  }
}
```

#### Alerting Rules

```yaml
# alerts.yml
groups:
  - name: agent_system
    rules:
      - alert: HighErrorRate
        expr: rate(agent_errors_total[5m]) > 0.1
        for: 5m
        annotations:
          summary: "High error rate detected"
      
      - alert: SlowResponse
        expr: histogram_quantile(0.95, agent_request_duration_seconds) > 30
        for: 5m
        annotations:
          summary: "Slow response time detected"
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Ollama Connection Failed

**Symptoms:**
```
Error: Could not connect to Ollama at http://localhost:11434
```

**Solutions:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve

# Check Ollama logs
journalctl -u ollama -f
```

#### Issue 2: Model Not Found

**Symptoms:**
```
Error: Model 'llama3.2' not found
```

**Solutions:**
```bash
# List available models
ollama list

# Pull missing model
ollama pull llama3.2
```

#### Issue 3: Out of Memory

**Symptoms:**
```
Error: CUDA out of memory
```

**Solutions:**
```bash
# Use smaller model
export DEFAULT_MODEL=llama2:7b

# Reduce batch size
export MAX_WORKERS=2

# Clear GPU memory
nvidia-smi --gpu-reset
```

#### Issue 4: Slow Response Times

**Symptoms:**
- Requests taking > 30 seconds

**Solutions:**
```python
# Enable caching
ENABLE_CACHING=true

# Use GPU acceleration
# Install CUDA and cuDNN

# Optimize model
ollama pull llama3.2:q4_0  # Quantized version
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python main.py --verbose

# Check logs
tail -f logs/agent_system.log
```

---

## Maintenance

### Regular Tasks

#### Daily
- Monitor system health
- Check error logs
- Verify backup completion

#### Weekly
- Review performance metrics
- Update dependencies
- Clean old logs

#### Monthly
- Update LLM models
- Review and optimize role files
- Security audit

### Update Procedure

```bash
# Backup current installation
./backup.sh

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Update models
ollama pull llama3.2

# Restart services
systemctl restart agent-system

# Verify
python tests/test_all_agents.py
```

### Scaling Guidelines

#### Vertical Scaling
- Increase CPU cores for parallel execution
- Add more RAM for larger models
- Use GPU for faster inference

#### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Use shared storage for role files
- Implement distributed caching

---

## Support

For deployment support:
- Documentation: [docs.yoursite.com](https://docs.yoursite.com)
- GitHub Issues: [github.com/yourrepo/issues](https://github.com/yourrepo/issues)
- Email: devops@yoursite.com

---

## Appendix

### A. System Requirements by Deployment Type

| Deployment | CPU | RAM | Storage | Network |
|------------|-----|-----|---------|---------|
| Development | 4 cores | 8 GB | 20 GB | 10 Mbps |
| Small Production | 8 cores | 16 GB | 50 GB | 100 Mbps |
| Medium Production | 16 cores | 32 GB | 100 GB | 1 Gbps |
| Large Production | 32+ cores | 64+ GB | 500+ GB | 10 Gbps |

### B. Recommended Models by Use Case

| Use Case | Model | Size | Performance |
|----------|-------|------|-------------|
| Development | llama3.2:7b | 4.7 GB | Fast |
| General Purpose | llama3.2 | 7.4 GB | Balanced |
| Code Generation | codellama | 7.4 GB | Specialized |
| High Accuracy | llama2:70b | 39 GB | Slow but accurate |

### C. Port Reference

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Ollama | 11434 | HTTP | LLM API |
| Application | 8000 | HTTP | Main API |
| Prometheus | 9090 | HTTP | Metrics |
| Grafana | 3000 | HTTP | Dashboard |
| Redis | 6379 | TCP | Caching |
