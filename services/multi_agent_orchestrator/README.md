# Multi-Agent Orchestrator Docker Service

## Overview

This Docker service runs the complete Multi-Agent Orchestrator system with all 29 specialized agents and the meeting system. It's optimized for production use with proper resource allocation and health monitoring.

## Features

- **All 29 Agents**: Complete agent system including developers, managers, architects, and specialists
- **Meeting System**: Full meeting orchestration with 20+ meeting types
- **Memory Management**: Persistent agent memories and conversation history
- **Health Monitoring**: Built-in health checks and logging
- **Resource Optimization**: Configured with optimal CPU and memory limits
- **Network Isolation**: Proper network segmentation for security

## Architecture

### Container Specifications

- **Base Image**: Python 3.11-slim (optimized for size and performance)
- **CPU Limit**: 4 cores (2 cores reserved)
- **Memory Limit**: 4GB (2GB reserved)
- **Storage**: Persistent volumes for memories and logs
- **Network**: Connected to both front-tier and back-tier networks

### Resource Allocation

The service is configured with the following resource limits:

```yaml
deploy:
  resources:
    limits:
      cpus: '4.0'      # Maximum 4 CPU cores
      memory: 4G       # Maximum 4GB RAM
    reservations:
      cpus: '2.0'      # Minimum 2 CPU cores reserved
      memory: 2G       # Minimum 2GB RAM reserved
```

### Why These Resources?

- **29 Agents**: Each agent requires memory for model loading and context
- **Meeting System**: Parallel agent execution during meetings requires CPU
- **Memory Management**: Agent memories and conversation history need storage
- **LLM Communication**: Network overhead for Ollama communication

## Quick Start

### 1. Build and Start the Service

```bash
# Build the service
docker-compose build multi_agent_orchestrator

# Start the service
docker-compose up -d multi_agent_orchestrator

# View logs
docker-compose logs -f multi_agent_orchestrator
```

### 2. Access the Service

```bash
# Enter the container
docker exec -it multi_agent_orchestrator bash

# Run interactive mode
python agents/interactive.py

# Run demo
python agents/demo.py

# Run main examples
python agents/main.py
```

### 3. Stop the Service

```bash
# Stop the service
docker-compose stop multi_agent_orchestrator

# Remove the service
docker-compose down multi_agent_orchestrator
```

## Environment Variables

The service uses the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://ollama:11434` | Ollama service URL |
| `MODEL_NAME` | `llama3.2` | Default LLM model |
| `TEMPERATURE` | `0.7` | LLM temperature setting |
| `PYTHONUNBUFFERED` | `1` | Unbuffered Python output |
| `PYTHONPATH` | `/app:/app/agents` | Python module path |

## Volumes

The service uses persistent volumes for data storage:

### orchestrator_data
- **Path**: `/app/agent_memories`
- **Purpose**: Store agent conversation histories and memories
- **Persistence**: Data persists across container restarts

### orchestrator_logs
- **Path**: `/app/logs`
- **Purpose**: Store application logs and debugging information
- **Persistence**: Logs persist across container restarts

### Bind Mounts
- `./agents` → `/app/agents` (Agent code)
- `./Role` → `/app/Role` (Agent role definitions)
- `./examples` → `/app/examples` (Example scripts)

## Health Checks

The service includes a health check that runs every 30 seconds:

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "from agents.orchestrator import AgentOrchestrator; print('OK')"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Health Check Status

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' multi_agent_orchestrator

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' multi_agent_orchestrator
```

## Usage Examples

### Example 1: Single Agent Chat

```bash
docker exec -it multi_agent_orchestrator python -c "
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()
response = orchestrator.chat_with_agent(
    'backend_developer',
    'What are REST API best practices?'
)
print(response)
"
```

### Example 2: Multi-Agent Consultation

```bash
docker exec -it multi_agent_orchestrator python -c "
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()
responses = orchestrator.multi_agent_consultation(
    'How to build a scalable microservices architecture?',
    ['solutions_architect', 'backend_developer', 'devops_engineer']
)
for agent, response in responses.items():
    print(f'{agent}: {response[:200]}...')
"
```

### Example 3: Conduct a Meeting

```bash
docker exec -it multi_agent_orchestrator python -c "
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType

orchestrator = AgentOrchestrator()
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.ARCHITECTURE_REVIEW,
    title='Microservices Architecture Review',
    description='Review proposed microservices architecture'
)

topics = [
    'Service boundaries',
    'Communication patterns',
    'Data consistency'
]

result = orchestrator.conduct_meeting(meeting, topics)
print(result['summary'])
"
```

## Monitoring

### View Logs

```bash
# Real-time logs
docker-compose logs -f multi_agent_orchestrator

# Last 100 lines
docker-compose logs --tail=100 multi_agent_orchestrator

# Logs since timestamp
docker-compose logs --since 2024-01-01T00:00:00 multi_agent_orchestrator
```

### Resource Usage

```bash
# Container stats
docker stats multi_agent_orchestrator

# Detailed resource usage
docker inspect multi_agent_orchestrator | grep -A 10 "Resources"
```

### Memory Usage

```bash
# Check memory usage inside container
docker exec multi_agent_orchestrator python -c "
import psutil
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'CPU: {psutil.cpu_percent()}%')
"
```

## Troubleshooting

### Service Won't Start

1. **Check Ollama dependency**:
   ```bash
   docker-compose ps ollama
   docker-compose logs ollama
   ```

2. **Check resource availability**:
   ```bash
   docker system df
   docker system prune  # If needed
   ```

3. **Check logs**:
   ```bash
   docker-compose logs multi_agent_orchestrator
   ```

### Out of Memory

If the service runs out of memory:

1. **Increase memory limit** in `docker-compose.yml`:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 6G  # Increase from 4G
   ```

2. **Reduce concurrent agents** in meetings
3. **Clear agent memories** periodically

### Slow Performance

1. **Increase CPU allocation**:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '6.0'  # Increase from 4.0
   ```

2. **Check Ollama performance**:
   ```bash
   docker stats ollama
   ```

3. **Optimize model selection** (use smaller models if needed)

### Connection Issues

1. **Check network connectivity**:
   ```bash
   docker exec multi_agent_orchestrator ping ollama
   docker exec multi_agent_orchestrator curl http://ollama:11434
   ```

2. **Verify environment variables**:
   ```bash
   docker exec multi_agent_orchestrator env | grep OLLAMA
   ```

## Performance Optimization

### Recommended System Requirements

- **CPU**: 4+ cores (8+ recommended for meetings)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB for images and volumes
- **Network**: Low-latency connection to Ollama

### Optimization Tips

1. **Use SSD storage** for volumes
2. **Allocate more CPU** for parallel agent execution
3. **Increase memory** if running large meetings
4. **Use faster models** for better response times
5. **Enable Docker BuildKit** for faster builds:
   ```bash
   export DOCKER_BUILDKIT=1
   ```

## Security Considerations

### Network Isolation

- Service is on both `front-tier` and `back-tier` networks
- Ollama communication is internal only
- No direct external access (except port 8000 for future API)

### Volume Permissions

```bash
# Set proper permissions
docker exec multi_agent_orchestrator chown -R root:root /app/agent_memories
docker exec multi_agent_orchestrator chmod 700 /app/agent_memories
```

### Environment Variables

- Never commit `.env` files with secrets
- Use Docker secrets for sensitive data in production
- Rotate credentials regularly

## Backup and Recovery

### Backup Agent Memories

```bash
# Backup memories
docker run --rm -v orchestrator_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/agent_memories_backup.tar.gz -C /data .

# Backup logs
docker run --rm -v orchestrator_logs:/data -v $(pwd):/backup \
  alpine tar czf /backup/logs_backup.tar.gz -C /data .
```

### Restore from Backup

```bash
# Restore memories
docker run --rm -v orchestrator_data:/data -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/agent_memories_backup.tar.gz"

# Restore logs
docker run --rm -v orchestrator_logs:/data -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/logs_backup.tar.gz"
```

## Scaling

### Horizontal Scaling

To run multiple instances:

```yaml
multi_agent_orchestrator:
  # ... existing config ...
  deploy:
    replicas: 3  # Run 3 instances
    resources:
      # ... resource limits ...
```

### Load Balancing

Add a load balancer (nginx) in front of multiple instances:

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - multi_agent_orchestrator
```

## Integration

### With Other Services

The orchestrator can integrate with:

- **Qdrant**: Vector database for semantic search
- **PostgreSQL**: Persistent storage for agent data
- **Redis**: Caching and session management
- **Prometheus**: Metrics and monitoring
- **Grafana**: Visualization and dashboards

### API Endpoint (Future)

Port 8000 is exposed for future REST API:

```yaml
ports:
  - "8000:8000"  # For future API endpoint
```

## Development

### Local Development

```bash
# Mount local code for development
docker-compose up -d multi_agent_orchestrator

# Make changes to code
# Changes are reflected immediately due to bind mounts

# Restart to apply changes
docker-compose restart multi_agent_orchestrator
```

### Debugging

```bash
# Enter container with bash
docker exec -it multi_agent_orchestrator bash

# Run Python debugger
docker exec -it multi_agent_orchestrator python -m pdb agents/main.py

# Check Python environment
docker exec -it multi_agent_orchestrator python -c "import sys; print(sys.path)"
```

## Maintenance

### Regular Maintenance Tasks

1. **Clear old logs** (weekly):
   ```bash
   docker exec multi_agent_orchestrator find /app/logs -type f -mtime +7 -delete
   ```

2. **Prune old memories** (monthly):
   ```bash
   docker exec multi_agent_orchestrator python -c "
   from agents.orchestrator import AgentOrchestrator
   orchestrator = AgentOrchestrator()
   orchestrator.clear_all_memories()
   "
   ```

3. **Update images** (monthly):
   ```bash
   docker-compose pull
   docker-compose build --no-cache multi_agent_orchestrator
   docker-compose up -d multi_agent_orchestrator
   ```

## Support

For issues and questions:

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: See `/docs` directory
- **Logs**: Check container logs for debugging

## License

See main project LICENSE file.
