# System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│  (main.py / interactive.py / demo.py / Your Application)        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Agent Orchestrator                          │
│  - Manages all agents                                           │
│  - Coordinates multi-agent interactions                         │
│  - Handles workflows and memory                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Agent Layer                               │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Backend    │  │   DevOps     │  │   Product    │         │
│  │  Developer   │  │   Engineer   │  │   Manager    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │      QA      │  │   Frontend   │  │     Data     │         │
│  │   Engineer   │  │  Developer   │  │   Engineer   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Base Agent Class                            │
│  - LLM initialization (Ollama)                                  │
│  - Conversation memory management                               │
│  - Common chat interface                                        │
│  - Role prompt integration                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Role Loader                                │
│  - Loads role definitions from Role folder                      │
│  - Parses role metadata                                         │
│  - Generates system prompts                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Role Definitions                            │
│                     (Role/*.txt files)                           │
│                                                                  │
│  - Software_Developer_Backend.txt                               │
│  - DevOps_Engineer.txt                                          │
│  - Product_Manager.txt                                          │
│  - QA_Test_Engineer.txt                                         │
│  - Software_Developer_Frontend.txt                              │
│  - Data_Engineer.txt                                            │
│  - ... (29 total role files)                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Backend (Ollama)                          │
│  - Local LLM execution                                          │
│  - Model: llama3.2, mistral, codellama, etc.                   │
│  - Configurable temperature and parameters                      │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Single Agent Interaction
```
User Query
    │
    ▼
Orchestrator.get_agent("backend_developer")
    │
    ▼
Backend Developer Agent
    │
    ▼
Base Agent.chat(query)
    │
    ├─► Load Role Prompt (from Role/Software_Developer_Backend.txt)
    ├─► Load Conversation History (from Memory)
    ├─► Construct Messages [System + History + User]
    │
    ▼
LLM (Ollama)
    │
    ▼
Response
    │
    ├─► Save to Memory
    │
    ▼
Return to User
```

### Multi-Agent Consultation
```
User Query
    │
    ▼
Orchestrator.multi_agent_consultation(query, [agent1, agent2, agent3])
    │
    ├─► Agent 1 (Backend Developer)
    │   └─► Process query → Response 1
    │
    ├─► Agent 2 (DevOps Engineer)
    │   └─► Process query → Response 2
    │
    └─► Agent 3 (Product Manager)
        └─► Process query → Response 3
    │
    ▼
Aggregate Responses
    │
    ▼
Return {agent1: response1, agent2: response2, agent3: response3}
```

### Collaborative Workflow
```
Task Description
    │
    ▼
Orchestrator.collaborative_task(task, workflow)
    │
    ▼
Step 1: Product Manager
    │ Input: Task Description
    │ Action: write_user_stories()
    │ Output: User Stories
    │
    ▼
Step 2: Backend Developer
    │ Input: Task + Previous Response (User Stories)
    │ Action: design_api()
    │ Output: API Design
    │
    ▼
Step 3: QA Engineer
    │ Input: Task + Previous Responses
    │ Action: create_test_plan()
    │ Output: Test Plan
    │
    ▼
Return [
    {agent: "product_manager", response: "..."},
    {agent: "backend_developer", response: "..."},
    {agent: "qa_engineer", response: "..."}
]
```

## Component Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                         Orchestrator                             │
│                                                                  │
│  agents = {                                                     │
│      "backend_developer": BackendDeveloperAgent,                │
│      "devops_engineer": DevOpsEngineerAgent,                    │
│      "product_manager": ProductManagerAgent,                    │
│      ...                                                        │
│  }                                                              │
│                                                                  │
│  Methods:                                                       │
│  - get_agent(name)                                             │
│  - list_agents()                                               │
│  - chat_with_agent(name, message)                              │
│  - multi_agent_consultation(query, agents)                     │
│  - collaborative_task(task, workflow)                          │
│  - clear_all_memories()                                        │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ manages
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Specialized Agents                          │
│                                                                  │
│  Each inherits from BaseAgent:                                  │
│                                                                  │
│  class BackendDeveloperAgent(BaseAgent):                        │
│      role_filename = "Software_Developer_Backend.txt"           │
│      methods:                                                   │
│          - review_code()                                        │
│          - design_api()                                         │
│          - suggest_architecture()                               │
│                                                                  │
│  class DevOpsEngineerAgent(BaseAgent):                          │
│      role_filename = "DevOps_Engineer.txt"                      │
│      methods:                                                   │
│          - create_ci_cd_pipeline()                              │
│          - review_infrastructure()                              │
│          - troubleshoot_deployment()                            │
│          - design_monitoring()                                  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ inherits from
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Base Agent                                │
│                                                                  │
│  Attributes:                                                    │
│  - role_filename: str                                           │
│  - role_loader: RoleLoader                                      │
│  - role_prompt: str                                             │
│  - role_metadata: dict                                          │
│  - llm: ChatOllama                                              │
│  - memory: ConversationBufferMemory                             │
│  - system_message: SystemMessage                                │
│                                                                  │
│  Methods:                                                       │
│  - chat(message) → str                                          │
│  - get_role_info() → dict                                       │
│  - clear_memory()                                               │
│  - get_conversation_history() → list                            │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ uses
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Role Loader                               │
│                                                                  │
│  Methods:                                                       │
│  - load_role(filename) → str                                    │
│  - get_role_prompt(filename) → str                              │
│  - list_available_roles() → list                                │
│  - get_role_metadata(filename) → dict                           │
└─────────────────────────────────────────────────────────────────┘
```

## Memory Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Memory Structure                        │
│                                                                  │
│  Each agent has independent memory:                             │
│                                                                  │
│  ConversationBufferMemory {                                     │
│      chat_history: [                                            │
│          HumanMessage("User query 1"),                          │
│          AIMessage("Agent response 1"),                         │
│          HumanMessage("User query 2"),                          │
│          AIMessage("Agent response 2"),                         │
│          ...                                                    │
│      ]                                                          │
│  }                                                              │
│                                                                  │
│  Memory Operations:                                             │
│  - save_context(input, output)  # Add to history               │
│  - load_memory_variables()      # Retrieve history             │
│  - clear()                       # Reset memory                │
└─────────────────────────────────────────────────────────────────┘
```

## File Organization

```
agents/
│
├── Core Components
│   ├── orchestrator.py          # Main coordinator
│   ├── utils/
│   │   ├── base_agent.py        # Base class
│   │   └── role_loader.py       # Role file handler
│   │
├── Agent Implementations
│   ├── backend_developer/
│   ├── devops_engineer/
│   ├── product_manager/
│   ├── qa_engineer/
│   ├── frontend_developer/
│   └── data_engineer/
│
├── User Interfaces
│   ├── main.py                  # Basic examples
│   ├── interactive.py           # CLI interface
│   └── demo.py                  # Comprehensive demos
│
├── Testing
│   └── tests/
│       ├── test_role_loader.py
│       └── test_orchestrator.py
│
├── Documentation
│   ├── README.md                # Main documentation
│   ├── QUICKSTART.md            # Quick start guide
│   ├── PROJECT_OVERVIEW.md      # Detailed overview
│   └── ARCHITECTURE.md          # This file
│
└── Configuration
    ├── requirements.txt         # Dependencies
    ├── .env.example             # Environment template
    └── .gitignore               # Git ignore rules
```

## Extension Points

### Adding New Agents

```
1. Create Agent Folder
   agents/new_agent/

2. Implement Agent Class
   agents/new_agent/agent.py
   └─► Inherit from BaseAgent
   └─► Specify role_filename
   └─► Add specialized methods

3. Create Package Init
   agents/new_agent/__init__.py

4. Register in Orchestrator
   orchestrator.py
   └─► Import agent class
   └─► Add to _initialize_agents()

5. Create Role File
   Role/New_Role.txt
   └─► Define role responsibilities
   └─► Specify expertise areas
```

### Custom Workflows

```
Define workflow steps:
workflow = [
    {
        "agent": "agent_name",
        "action": "method_name"  # or "chat" for general
    },
    ...
]

Execute:
results = orchestrator.collaborative_task(task, workflow)

Each step receives:
- Original task description
- All previous agent responses
```

## Integration Patterns

### Pattern 1: Embedded Agent
```python
# Integrate into your application
from agents.orchestrator import AgentOrchestrator

class MyApp:
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
    
    def get_code_review(self, code):
        agent = self.orchestrator.get_agent("backend_developer")
        return agent.review_code(code)
```

### Pattern 2: API Wrapper
```python
# Create REST API endpoints
from flask import Flask, request
from agents.orchestrator import AgentOrchestrator

app = Flask(__name__)
orchestrator = AgentOrchestrator()

@app.route('/agent/<agent_name>/chat', methods=['POST'])
def chat(agent_name):
    message = request.json['message']
    response = orchestrator.chat_with_agent(agent_name, message)
    return {'response': response}
```

### Pattern 3: CLI Tool
```python
# Command-line interface
import click
from agents.orchestrator import AgentOrchestrator

@click.command()
@click.option('--agent', required=True)
@click.option('--message', required=True)
def chat(agent, message):
    orchestrator = AgentOrchestrator()
    response = orchestrator.chat_with_agent(agent, message)
    click.echo(response)
```

This architecture provides flexibility, extensibility, and clear separation of concerns for building sophisticated multi-agent AI systems.
