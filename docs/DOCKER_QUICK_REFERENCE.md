# Multi-Agent Orchestrator Docker Service - Quick Reference

## 🚀 Quick Start

### Start the Service

```bash
# Linux/Mac
./orchestrator.sh start

# Windows
orchestrator.bat start

# Manual
docker-compose up -d ollama multi_agent_orchestrator
```

### Stop the Service

```bash
# Linux/Mac
./orchestrator.sh stop

# Windows
orchestrator.bat stop

# Manual
docker-compose stop multi_agent_orchestrator
```

## 📋 Common Commands

### Management

| Action | Linux/Mac | Windows | Manual |
|--------|-----------|---------|--------|
| Build | `./orchestrator.sh build` | `orchestrator.bat build` | `docker-compose build multi_agent_orchestrator` |
| Start | `./orchestrator.sh start` | `orchestrator.bat start` | `docker-compose up -d multi_agent_orchestrator` |
| Stop | `./orchestrator.sh stop` | `orchestrator.bat stop` | `docker-compose stop multi_agent_orchestrator` |
| Restart | `./orchestrator.sh restart` | `orchestrator.bat restart` | `docker-compose restart multi_agent_orchestrator` |
| Status | `./orchestrator.sh status` | `orchestrator.bat status` | `docker ps \| grep multi_agent_orchestrator` |
| Logs | `./orchestrator.sh logs` | `orchestrator.bat logs` | `docker-compose logs -f multi_agent_orchestrator` |

### Usage

| Action | Linux/Mac | Windows | Manual |
|--------|-----------|---------|--------|
| Shell | `./orchestrator.sh shell` | `orchestrator.bat shell` | `docker exec -it multi_agent_orchestrator bash` |
| Interactive | `./orchestrator.sh interactive` | `orchestrator.bat interactive` | `docker exec -it multi_agent_orchestrator python agents/interactive.py` |
| Demo | `./orchestrator.sh demo` | `orchestrator.bat demo` | `docker exec -it multi_agent_orchestrator python agents/demo.py` |
| Examples | `./orchestrator.sh examples` | `orchestrator.bat examples` | `docker exec -it multi_agent_orchestrator python agents/main.py` |

### Maintenance

| Action | Linux/Mac | Windows | Manual |
|--------|-----------|---------|--------|
| Backup | `./orchestrator.sh backup` | `orchestrator.bat backup` | See [Backup Section](#backup) |
| Restore | `./orchestrator.sh restore DIR` | `orchestrator.bat restore DIR` | See [Restore Section](#restore) |
| Cleanup | `./orchestrator.sh cleanup` | `orchestrator.bat cleanup` | `docker-compose down multi_agent_orchestrator` |

## 🎯 Usage Examples

### Single Agent Chat

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

### Multi-Agent Consultation

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

### Conduct a Meeting

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

topics = ['Service boundaries', 'Communication patterns', 'Data consistency']
result = orchestrator.conduct_meeting(meeting, topics)
print(result['summary'])
"
```

## 📊 Monitoring

### Check Health

```bash
# Health status
docker inspect --format='{{.State.Health.Status}}' multi_agent_orchestrator

# Health logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' multi_agent_orchestrator
```

### Resource Usage

```bash
# Real-time stats
docker stats multi_agent_orchestrator

# CPU and Memory
docker exec multi_agent_orchestrator python -c "
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'Memory: {psutil.virtual_memory().percent}%')
"
```

### View Logs

```bash
# Real-time logs
docker-compose logs -f multi_agent_orchestrator

# Last 100 lines
docker-compose logs --tail=100 multi_agent_orchestrator

# Since timestamp
docker-compose logs --since 2024-01-01T00:00:00 multi_agent_orchestrator
```

## 💾 Backup and Restore

### Backup

```bash
# Create backup directory
mkdir -p backups/$(date +%Y%m%d_%H%M%S)

# Backup agent memories
docker run --rm -v orchestrator_data:/data -v $(pwd)/backups:/backup \
  alpine tar czf /backup/agent_memories_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .

# Backup logs
docker run --rm -v orchestrator_logs:/data -v $(pwd)/backups:/backup \
  alpine tar czf /backup/logs_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

### Restore

```bash
# Restore agent memories
docker run --rm -v orchestrator_data:/data -v $(pwd)/backups:/backup \
  alpine sh -c "cd /data && tar xzf /backup/agent_memories_TIMESTAMP.tar.gz"

# Restore logs
docker run --rm -v orchestrator_logs:/data -v $(pwd)/backups:/backup \
  alpine sh -c "cd /data && tar xzf /backup/logs_TIMESTAMP.tar.gz"
```

## 🔧 Troubleshooting

### Service Won't Start

```bash
# Check Docker
docker --version
docker-compose --version

# Check Ollama
docker-compose ps ollama
docker-compose logs ollama

# Check resources
docker system df
docker system prune  # If needed

# Check logs
docker-compose logs multi_agent_orchestrator
```

### Out of Memory

Edit `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 6G  # Increase from 4G
```

Then restart:

```bash
docker-compose up -d multi_agent_orchestrator
```

### Slow Performance

Edit `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '6.0'  # Increase from 4.0
```

Then restart:

```bash
docker-compose up -d multi_agent_orchestrator
```

### Connection Issues

```bash
# Check network
docker exec multi_agent_orchestrator ping ollama

# Check Ollama
docker exec multi_agent_orchestrator curl http://ollama:11434

# Check environment
docker exec multi_agent_orchestrator env | grep OLLAMA
```

## 📈 Resource Allocation

### Current Configuration

- **CPU**: 4 cores max (2 cores reserved)
- **Memory**: 4GB max (2GB reserved)
- **Storage**: Unlimited (host-dependent)
- **Network**: front-tier + back-tier

### Recommended for Production

- **CPU**: 8 cores
- **Memory**: 8GB
- **Storage**: 50GB SSD
- **Network**: Dedicated network

### Scaling Up

Edit `docker-compose.yml`:

```yaml
multi_agent_orchestrator:
  deploy:
    replicas: 3  # Run 3 instances
    resources:
      limits:
        cpus: '8.0'
        memory: 8G
      reservations:
        cpus: '4.0'
        memory: 4G
```

## 🔒 Security

### Network Isolation

- Service on front-tier and back-tier networks
- Ollama communication internal only
- No direct external access (except port 8000)

### Volume Permissions

```bash
# Set proper permissions
docker exec multi_agent_orchestrator chown -R root:root /app/agent_memories
docker exec multi_agent_orchestrator chmod 700 /app/agent_memories
```

### Environment Variables

- Never commit `.env` files
- Use Docker secrets in production
- Rotate credentials regularly

## 📚 Documentation

- **Service README**: `services/multi_agent_orchestrator/README.md`
- **Deployment Guide**: `docs/DEPLOYMENT_GUIDE.md`
- **Implementation Summary**: `docs/DOCKER_SERVICE_SUMMARY.md`
- **Main README**: `README.md`

## 🆘 Support

### Common Issues

1. **Service won't start**: Check Docker and Ollama
2. **Out of memory**: Increase memory limit
3. **Slow performance**: Increase CPU allocation
4. **Connection issues**: Check network and environment

### Getting Help

- Check logs: `docker-compose logs multi_agent_orchestrator`
- Check status: `docker ps | grep multi_agent_orchestrator`
- Check health: `docker inspect multi_agent_orchestrator`
- Read documentation: `services/multi_agent_orchestrator/README.md`

## 🎉 Quick Tips

1. **Use scripts**: `./orchestrator.sh` or `orchestrator.bat` for easy management
2. **Monitor resources**: Use `docker stats` to watch resource usage
3. **Backup regularly**: Use `./orchestrator.sh backup` weekly
4. **Check health**: Use `./orchestrator.sh status` to verify service health
5. **View logs**: Use `./orchestrator.sh logs` for debugging
6. **Use SSD**: Store volumes on SSD for better performance
7. **Allocate more resources**: Increase CPU/memory for production
8. **Keep updated**: Regularly update Docker images

---

**Quick Start**: `./orchestrator.sh start` or `orchestrator.bat start`  
**Documentation**: `services/multi_agent_orchestrator/README.md`  
**Support**: Check logs and documentation first
