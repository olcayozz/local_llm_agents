# API Reference Documentation

## Overview

Complete API reference for the Multi-Agent Orchestrator System. This document covers all public methods, classes, and interfaces.

## Table of Contents

1. [AgentOrchestrator](#agentorchestrator)
2. [BaseAgent](#baseagent)
3. [Meeting System](#meeting-system)
4. [Role Loader](#role-loader)
5. [Data Models](#data-models)
6. [Enumerations](#enumerations)

---

## AgentOrchestrator

The main orchestrator class that manages all 29 agents and coordinates their interactions.

### Class Definition

```python
class AgentOrchestrator:
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    )
```

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_name` | `str` | `"llama3.2"` | Ollama model name to use |
| `temperature` | `float` | `0.7` | LLM temperature (0.0-1.0) |
| `role_folder` | `str` | `"Role"` | Path to role definition files |

### Methods

#### chat_with_agent

Chat with a specific agent.

```python
def chat_with_agent(
    self,
    agent_name: str,
    message: str
) -> str
```

**Parameters:**
- `agent_name` (str): Name of the agent to chat with
- `message` (str): User message/query

**Returns:**
- `str`: Agent's response

**Raises:**
- `ValueError`: If agent_name is not found

**Example:**
```python
orchestrator = AgentOrchestrator()
response = orchestrator.chat_with_agent(
    "backend_developer",
    "How should I design a REST API?"
)
print(response)
```

---

#### multi_agent_consultation

Consult multiple agents in parallel on the same query.

```python
def multi_agent_consultation(
    self,
    query: str,
    agent_names: List[str]
) -> Dict[str, str]
```

**Parameters:**
- `query` (str): Question or task for all agents
- `agent_names` (List[str]): List of agent names to consult

**Returns:**
- `Dict[str, str]`: Dictionary mapping agent names to their responses

**Example:**
```python
responses = orchestrator.multi_agent_consultation(
    query="How should we implement authentication?",
    agent_names=["backend_developer", "security_engineer", "database_administrator"]
)

for agent, response in responses.items():
    print(f"{agent}: {response}")
```

---

#### collaborative_task

Execute a task with multiple agents in sequence, building context.

```python
def collaborative_task(
    self,
    task_description: str,
    workflow: List[Dict[str, str]]
) -> List[Dict[str, str]]
```

**Parameters:**
- `task_description` (str): Overall task description
- `workflow` (List[Dict]): List of workflow steps with agent names

**Returns:**
- `List[Dict[str, str]]`: List of results with agent names and responses

**Example:**
```python
workflow = [
    {"agent": "product_manager", "action": "chat"},
    {"agent": "solutions_architect", "action": "chat"},
    {"agent": "backend_developer", "action": "chat"}
]

results = orchestrator.collaborative_task(
    task_description="Design a payment processing system",
    workflow=workflow
)
```

---

#### create_meeting

Create a new meeting with automatic participant selection.

```python
def create_meeting(
    self,
    meeting_type: MeetingType,
    title: str,
    description: str = "",
    custom_participants: Optional[List[str]] = None
) -> Meeting
```

**Parameters:**
- `meeting_type` (MeetingType): Type of meeting (enum)
- `title` (str): Meeting title
- `description` (str, optional): Meeting description
- `custom_participants` (List[str], optional): Override default participants

**Returns:**
- `Meeting`: Meeting object

**Example:**
```python
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Sprint 24 Planning",
    description="Plan deliverables for next sprint"
)
```

---

#### conduct_meeting

Conduct a meeting with specified topics.

```python
def conduct_meeting(
    self,
    meeting: Meeting,
    topics: List[str]
) -> Dict[str, Any]
```

**Parameters:**
- `meeting` (Meeting): Meeting object
- `topics` (List[str]): List of discussion topics

**Returns:**
- `Dict[str, Any]`: Meeting results with responses per topic

**Example:**
```python
topics = [
    "User Story: OAuth2 authentication",
    "Technical debt: Refactor payment service"
]

result = orchestrator.conduct_meeting(meeting, topics)
```

---

#### list_agents

Get list of all available agents.

```python
def list_agents(self) -> List[str]
```

**Returns:**
- `List[str]`: List of agent names

**Example:**
```python
agents = orchestrator.list_agents()
print(f"Available agents: {len(agents)}")
```

---

#### get_agent_info

Get information about a specific agent.

```python
def get_agent_info(self, agent_name: str) -> Dict[str, str]
```

**Parameters:**
- `agent_name` (str): Name of the agent

**Returns:**
- `Dict[str, str]`: Agent information (role, description, etc.)

**Example:**
```python
info = orchestrator.get_agent_info("backend_developer")
print(f"Role: {info['role']}")
print(f"Description: {info['description']}")
```

---

#### clear_agent_memory

Clear conversation history for a specific agent.

```python
def clear_agent_memory(self, agent_name: str) -> None
```

**Parameters:**
- `agent_name` (str): Name of the agent

**Example:**
```python
orchestrator.clear_agent_memory("backend_developer")
```

---

#### clear_all_memories

Clear conversation history for all agents.

```python
def clear_all_memories(self) -> None
```

**Example:**
```python
orchestrator.clear_all_memories()
```

---

#### get_meeting_summary

Get formatted summary of a meeting.

```python
def get_meeting_summary(self, meeting: Meeting) -> str
```

**Parameters:**
- `meeting` (Meeting): Meeting object

**Returns:**
- `str`: Formatted meeting summary

**Example:**
```python
summary = orchestrator.get_meeting_summary(meeting)
print(summary)
```

---

#### list_meetings

Get list of all meetings.

```python
def list_meetings(self) -> List[Meeting]
```

**Returns:**
- `List[Meeting]`: List of all meeting objects

---

#### get_available_meeting_types

Get list of available meeting types.

```python
def get_available_meeting_types(self) -> List[str]
```

**Returns:**
- `List[str]`: List of meeting type names

---

#### get_meeting_participants_for_type

Get default participants for a meeting type.

```python
def get_meeting_participants_for_type(
    self,
    meeting_type: MeetingType
) -> List[str]
```

**Parameters:**
- `meeting_type` (MeetingType): Meeting type enum

**Returns:**
- `List[str]`: List of agent names

---

## BaseAgent

Base class for all agents. All 29 agents inherit from this class.

### Class Definition

```python
class BaseAgent:
    def __init__(
        self,
        role_filename: str,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    )
```

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `role_filename` | `str` | Required | Role definition file name |
| `model_name` | `str` | `"llama3.2"` | Ollama model name |
| `temperature` | `float` | `0.7` | LLM temperature |
| `role_folder` | `str` | `"Role"` | Role files directory |

### Methods

#### chat

Send a message to the agent.

```python
def chat(self, message: str) -> str
```

**Parameters:**
- `message` (str): User message

**Returns:**
- `str`: Agent response

---

#### get_role_info

Get agent's role information.

```python
def get_role_info(self) -> Dict[str, str]
```

**Returns:**
- `Dict[str, str]`: Role information

---

#### clear_memory

Clear agent's conversation history.

```python
def clear_memory(self) -> None
```

---

## Meeting System

### Meeting Class

```python
class Meeting:
    def __init__(
        self,
        meeting_type: MeetingType,
        title: str,
        description: str = "",
        participants: Optional[List[str]] = None
    )
```

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `str` | Unique meeting ID (UUID) |
| `meeting_type` | `MeetingType` | Type of meeting |
| `title` | `str` | Meeting title |
| `description` | `str` | Meeting description |
| `participants` | `List[str]` | List of participant agent names |
| `start_time` | `datetime` | Meeting start time |
| `end_time` | `Optional[datetime]` | Meeting end time |
| `agenda` | `List[str]` | Meeting agenda items |
| `discussions` | `Dict[str, List[Dict]]` | Topic discussions |
| `decisions` | `List[str]` | Decisions made |
| `action_items` | `List[Dict]` | Action items |
| `status` | `str` | Meeting status |

#### Methods

##### add_agenda_item

```python
def add_agenda_item(self, item: str) -> None
```

##### add_discussion

```python
def add_discussion(
    self,
    topic: str,
    agent: str,
    response: str
) -> None
```

##### add_decision

```python
def add_decision(self, decision: str) -> None
```

##### add_action_item

```python
def add_action_item(
    self,
    assignee: str,
    task: str,
    due_date: Optional[datetime] = None
) -> None
```

##### complete_meeting

```python
def complete_meeting(self) -> None
```

##### get_summary

```python
def get_summary(self) -> str
```

---

### MeetingParticipantSelector

```python
class MeetingParticipantSelector:
    @staticmethod
    def select_participants(
        meeting_type: MeetingType,
        custom_participants: Optional[List[str]] = None
    ) -> List[str]
```

**Parameters:**
- `meeting_type` (MeetingType): Type of meeting
- `custom_participants` (List[str], optional): Override participants

**Returns:**
- `List[str]`: List of participant agent names

---

## Role Loader

### RoleLoader Class

```python
class RoleLoader:
    @staticmethod
    def load_role(
        role_filename: str,
        role_folder: str = "Role"
    ) -> str
```

**Parameters:**
- `role_filename` (str): Role file name
- `role_folder` (str): Role files directory

**Returns:**
- `str`: Role definition content

**Raises:**
- `FileNotFoundError`: If role file not found

---

## Data Models

### ActionItem

```python
@dataclass
class ActionItem:
    id: str
    assignee: str
    task: str
    due_date: Optional[datetime]
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
```

### Discussion

```python
@dataclass
class Discussion:
    topic: str
    agent: str
    response: str
    timestamp: datetime = field(default_factory=datetime.now)
```

### AgentInfo

```python
@dataclass
class AgentInfo:
    name: str
    role: str
    description: str
    specializations: List[str]
```

---

## Enumerations

### MeetingType

```python
class MeetingType(Enum):
    # Agile/Scrum Meetings
    DAILY_STANDUP = "daily_standup"
    SPRINT_PLANNING = "sprint_planning"
    SPRINT_REVIEW = "sprint_review"
    SPRINT_RETROSPECTIVE = "sprint_retrospective"
    BACKLOG_REFINEMENT = "backlog_refinement"
    
    # Technical Meetings
    ARCHITECTURE_REVIEW = "architecture_review"
    CODE_REVIEW = "code_review"
    TECHNICAL_DESIGN = "technical_design"
    SECURITY_REVIEW = "security_review"
    DATABASE_REVIEW = "database_review"
    
    # Planning Meetings
    STEERCO = "steerco"
    WEEKLY_STATUS = "weekly_status"
    PRODUCT_ROADMAP = "product_roadmap"
    RELEASE_PLANNING = "release_planning"
    QUARTERLY_PLANNING = "quarterly_planning"
    
    # Operations Meetings
    DEPLOYMENT_PLANNING = "deployment_planning"
    CAPACITY_PLANNING = "capacity_planning"
    INCIDENT_POSTMORTEM = "incident_postmortem"
    
    # Knowledge Sharing
    KNOWLEDGE_SHARING = "knowledge_sharing"
    ONBOARDING = "onboarding"
    PERFORMANCE_REVIEW = "performance_review"
```

---

## Error Handling

### Common Exceptions

#### ValueError
Raised when invalid agent name or meeting type is provided.

```python
try:
    response = orchestrator.chat_with_agent("invalid_agent", "Hello")
except ValueError as e:
    print(f"Error: {e}")
```

#### FileNotFoundError
Raised when role file is not found.

```python
try:
    role = RoleLoader.load_role("NonExistent.txt")
except FileNotFoundError as e:
    print(f"Error: {e}")
```

---

## Usage Examples

### Example 1: Simple Agent Chat

```python
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

response = orchestrator.chat_with_agent(
    "backend_developer",
    "What's the best way to handle authentication?"
)

print(response)
```

### Example 2: Multi-Agent Consultation

```python
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

responses = orchestrator.multi_agent_consultation(
    query="How should we design a microservices architecture?",
    agent_names=[
        "solutions_architect",
        "cloud_architect",
        "backend_developer",
        "devops_engineer"
    ]
)

for agent, response in responses.items():
    print(f"\n{agent.upper()}:")
    print(response)
```

### Example 3: Conducting a Meeting

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType
from datetime import datetime, timedelta

orchestrator = AgentOrchestrator()

# Create meeting
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Sprint 24 Planning",
    description="Plan deliverables for next sprint"
)

# Conduct meeting
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

### Example 4: Collaborative Workflow

```python
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

workflow = [
    {"agent": "product_manager", "action": "chat"},
    {"agent": "solutions_architect", "action": "chat"},
    {"agent": "backend_developer", "action": "chat"},
    {"agent": "security_engineer", "action": "chat"},
    {"agent": "devops_engineer", "action": "chat"}
]

results = orchestrator.collaborative_task(
    task_description="Design a secure payment processing system",
    workflow=workflow
)

for result in results:
    print(f"\n{result['agent'].upper()}:")
    print(result['response'])
```

### Example 5: Custom Meeting Participants

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType

orchestrator = AgentOrchestrator()

# Override default participants
custom_participants = [
    "cto",
    "engineering_manager",
    "solutions_architect",
    "security_engineer"
]

meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.ARCHITECTURE_REVIEW,
    title="Security Architecture Review",
    description="Review security architecture for new features",
    custom_participants=custom_participants
)

topics = ["Authentication flow", "Data encryption", "API security"]
result = orchestrator.conduct_meeting(meeting, topics)
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_HOST` | Ollama server URL | `http://localhost:11434` |
| `ROLE_FOLDER` | Path to role files | `Role` |
| `DEFAULT_MODEL` | Default LLM model | `llama3.2` |
| `DEFAULT_TEMPERATURE` | Default temperature | `0.7` |

### Configuration File

Create a `config.yaml` file:

```yaml
orchestrator:
  model_name: "llama3.2"
  temperature: 0.7
  role_folder: "Role"

ollama:
  host: "http://localhost:11434"
  timeout: 300

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## Best Practices

### 1. Agent Selection
- Choose agents based on their expertise
- Use multi-agent consultation for complex decisions
- Consider meeting types for structured discussions

### 2. Memory Management
- Clear agent memory periodically to prevent context overflow
- Use separate agent instances for different contexts
- Monitor memory usage for long conversations

### 3. Error Handling
- Always wrap agent calls in try-except blocks
- Validate agent names before calling
- Handle timeout scenarios for long-running tasks

### 4. Performance
- Use parallel execution for independent agent queries
- Cache frequently used responses
- Optimize role file loading

### 5. Security
- Sanitize user inputs before passing to agents
- Implement rate limiting for API calls
- Audit agent interactions for sensitive data

---

## Rate Limits

| Operation | Limit | Window |
|-----------|-------|--------|
| Agent Chat | 100 requests | 1 minute |
| Multi-Agent Consultation | 10 requests | 1 minute |
| Meeting Creation | 50 meetings | 1 hour |
| Meeting Conduct | 20 meetings | 1 hour |

---

## Versioning

Current API Version: **v1.0.0**

### Version History

- **v1.0.0** (2024-01-15): Initial release with 29 agents
- **v0.9.0** (2024-01-10): Beta release with 6 agents
- **v0.5.0** (2024-01-05): Alpha release with meeting system

---

## Support

For API support and questions:
- GitHub Issues: [github.com/yourrepo/issues](https://github.com/yourrepo/issues)
- Documentation: [docs.yoursite.com](https://docs.yoursite.com)
- Email: support@yoursite.com

---

## License

This API is licensed under [Your License]. See LICENSE file for details.
