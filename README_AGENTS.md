# Multi-Agent Orchestrator System

## Overview

A comprehensive multi-agent AI system featuring **29 specialized agents** powered by local LLMs (Ollama). Each agent has a unique role and expertise, enabling complex collaborative workflows and intelligent meeting facilitation.

## 🎯 Key Features

- **29 Specialized Agents**: Complete coverage of software development, operations, data, and management roles
- **Intelligent Meeting System**: Automated participant selection for 20+ meeting types
- **Collaborative Workflows**: Multi-agent task execution with context sharing
- **Role-Based Behavior**: Each agent uses specialized role definitions
- **Memory Management**: Conversation history tracking per agent
- **Local LLM Integration**: Powered by Ollama (llama3.2 by default)

## 📋 All 29 Agents

### Development Team (9)
- Backend Developer
- Frontend Developer
- Full Stack Developer
- Mobile Developer (Android)
- Mobile Developer (iOS)
- QA Engineer
- UI/UX Designer
- Technical Writer
- Security Engineer

### Operations & Infrastructure (7)
- DevOps Engineer
- Site Reliability Engineer
- Network Engineer
- System Administrator
- Cloud Architect
- Solutions Architect
- DevOps Manager

### Data & Analytics (4)
- Data Engineer
- Data Analyst
- Business Intelligence Analyst
- Database Administrator

### Management & Leadership (6)
- Product Manager
- Project Manager
- Scrum Master
- Engineering Manager
- IT Manager
- CTO/CIO

### IT Support (3)
- IT Support L1
- IT Support L2
- IT Support L3

## 🚀 Quick Start

### Prerequisites

```bash
# Install Ollama
# Visit: https://ollama.ai

# Pull the model
ollama pull llama3.2

# Install Python dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from agents.orchestrator import AgentOrchestrator

# Initialize orchestrator with all 29 agents
orchestrator = AgentOrchestrator()

# List all available agents
agents = orchestrator.list_agents()
print(f"Available agents: {len(agents)}")

# Chat with a specific agent
response = orchestrator.chat_with_agent(
    "backend_developer",
    "How should I design a REST API?"
)
print(response)

# Multi-agent consultation
responses = orchestrator.multi_agent_consultation(
    query="How should we implement user authentication?",
    agent_names=["backend_developer", "security_engineer", "database_administrator"]
)

for agent, response in responses.items():
    print(f"\n{agent}: {response}")
```

## 🤝 Meeting System

### Create and Conduct Meetings

```python
from agents.utils.meeting import MeetingType

# Create a meeting with automatic participant selection
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Sprint 24 Planning",
    description="Plan deliverables for next sprint"
)

# Conduct the meeting
topics = [
    "User Story: OAuth2 authentication",
    "User Story: Real-time notifications",
    "Technical debt: Refactor payment service"
]

result = orchestrator.conduct_meeting(meeting, topics)

# Add outcomes
meeting.add_action_item(
    assignee="backend_developer",
    task="Implement OAuth2 endpoints",
    due_date=datetime.now() + timedelta(days=7)
)

meeting.add_decision("Approved OAuth2 implementation approach")

# Get summary
summary = orchestrator.get_meeting_summary(meeting)
print(summary)
```

### Available Meeting Types

- **Agile/Scrum**: Daily Standup, Sprint Planning, Sprint Review, Sprint Retrospective
- **Technical**: Architecture Review, Code Review, Technical Design, Security Review
- **Planning**: Steerco, Weekly Status, Product Roadmap, Release Planning
- **Operations**: Deployment Planning, Capacity Planning, Incident Postmortem
- **Knowledge**: Knowledge Sharing, Onboarding, Performance Review

## 🔄 Collaborative Workflows

```python
# Define a workflow with multiple agents
workflow = [
    {"agent": "product_manager", "action": "chat"},
    {"agent": "solutions_architect", "action": "chat"},
    {"agent": "backend_developer", "action": "chat"},
    {"agent": "security_engineer", "action": "chat"},
    {"agent": "devops_engineer", "action": "chat"}
]

# Execute collaborative task
results = orchestrator.collaborative_task(
    task_description="Design a secure payment processing system",
    workflow=workflow
)

# Each agent builds on previous responses
for result in results:
    print(f"\n{result['agent']}: {result['response'][:200]}...")
```

## 📁 Project Structure

```
local_llm_agents/
├── agents/
│   ├── backend_developer/
│   ├── frontend_developer/
│   ├── fullstack_developer/
│   ├── mobile_developer_android/
│   ├── mobile_developer_ios/
│   ├── devops_engineer/
│   ├── security_engineer/
│   ├── ... (all 29 agents)
│   ├── utils/
│   │   ├── base_agent.py
│   │   ├── role_loader.py
│   │   └── meeting.py
│   └── orchestrator.py
├── Role/
│   ├── Software_Developer_Backend.txt
│   ├── Software_Developer_Frontend.txt
│   ├── ... (all 29 role files)
├── docs/
│   ├── ALL_AGENTS_SUMMARY.md
│   ├── MEETING_SYSTEM.md
│   ├── MEETING_QUICK_REFERENCE.md
│   └── MEETING_IMPLEMENTATION_SUMMARY.md
├── examples/
│   └── meeting_examples.py
├── tests/
│   ├── test_all_agents.py
│   └── test_meeting_system.py
└── requirements.txt
```

## 🧪 Testing

```bash
# Test all agents
python tests/test_all_agents.py

# Test meeting system
python tests/test_meeting_system.py

# Run examples
python examples/meeting_examples.py
```

## 📚 Documentation

- **[All Agents Summary](docs/ALL_AGENTS_SUMMARY.md)** - Complete list of all 29 agents
- **[Meeting System](docs/MEETING_SYSTEM.md)** - Full meeting system documentation
- **[Quick Reference](docs/MEETING_QUICK_REFERENCE.md)** - Quick reference guide
- **[Implementation Summary](docs/MEETING_IMPLEMENTATION_SUMMARY.md)** - Technical details

## 🎨 Use Cases

### 1. Code Review
```python
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.CODE_REVIEW,
    title="Security Code Review",
    description="Review authentication implementation"
)

topics = ["OAuth2 implementation", "Token management", "API security"]
result = orchestrator.conduct_meeting(meeting, topics)
```

### 2. Architecture Design
```python
responses = orchestrator.multi_agent_consultation(
    query="Design a microservices architecture for e-commerce platform",
    agent_names=[
        "solutions_architect",
        "cloud_architect",
        "backend_developer",
        "database_administrator",
        "security_engineer"
    ]
)
```

### 3. Incident Response
```python
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.INCIDENT_POSTMORTEM,
    title="Production Outage Postmortem",
    description="Analyze and prevent future incidents"
)

topics = [
    "Root cause analysis",
    "Timeline of events",
    "Prevention measures",
    "Action items"
]

result = orchestrator.conduct_meeting(meeting, topics)
```

### 4. Sprint Planning
```python
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Sprint 25 Planning",
    description="Plan next sprint deliverables"
)

# Automatically includes: scrum_master, product_manager, developers, qa, devops, ui_ux_designer

topics = [
    "User Story: Payment gateway integration",
    "User Story: Mobile app notifications",
    "Technical debt: Database optimization"
]

result = orchestrator.conduct_meeting(meeting, topics)
```

## ⚙️ Configuration

### Custom Model

```python
orchestrator = AgentOrchestrator(
    model_name="mistral",  # or any Ollama model
    temperature=0.7,
    role_folder="Role"
)
```

### Custom Role Files

Place custom role files in the `Role/` directory with `.txt` extension.

## 🔧 Advanced Features

### Memory Management

```python
# Clear specific agent memory
orchestrator.clear_agent_memory("backend_developer")

# Clear all agent memories
orchestrator.clear_all_memories()
```

### Agent Information

```python
# Get agent role information
info = orchestrator.get_agent_info("security_engineer")
print(info['role'])
print(info['description'])
```

### Meeting Management

```python
# List all meetings
meetings = orchestrator.list_meetings()

# Get available meeting types
types = orchestrator.get_available_meeting_types()

# Get participants for a meeting type
participants = orchestrator.get_meeting_participants_for_type(
    MeetingType.ARCHITECTURE_REVIEW
)
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. Add more specialized agents
2. Create new meeting types
3. Implement agent tools and integrations
4. Add more workflow templates
5. Improve role definitions

## 📝 License

[Your License Here]

## 🙏 Acknowledgments

- Powered by [Ollama](https://ollama.ai)
- Built with [LangChain](https://langchain.com)

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ for collaborative AI development**
