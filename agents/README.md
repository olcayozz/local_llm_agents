# Multi-Agent System with LangChain

A sophisticated multi-agent system where each AI agent acts according to specific roles defined in the `Role` folder. Built with LangChain and designed for local LLM integration (Ollama).

## Project Structure

```
agents/
├── utils/
│   ├── role_loader.py          # Loads role definitions from Role folder
│   └── base_agent.py            # Base agent class with common functionality
├── backend_developer/
│   └── agent.py                 # Backend Developer agent
├── devops_engineer/
│   └── agent.py                 # DevOps Engineer agent
├── product_manager/
│   └── agent.py                 # Product Manager agent
├── qa_engineer/
│   └── agent.py                 # QA Engineer agent
├── frontend_developer/
│   └── agent.py                 # Frontend Developer agent
├── data_engineer/
│   └── agent.py                 # Data Engineer agent
├── orchestrator.py              # Main orchestrator for managing agents
├── main.py                      # Example usage script
└── requirements.txt             # Python dependencies
```

## Features

- **Role-Based Agents**: Each agent imports and acts according to role definitions from the `Role` folder
- **Specialized Methods**: Each agent has domain-specific methods (e.g., code review, API design, test planning)
- **Memory Management**: Conversation history maintained per agent
- **Multi-Agent Collaboration**: Agents can work together on complex tasks
- **Flexible Orchestration**: Easy coordination between multiple agents
- **Local LLM Support**: Uses Ollama for running models locally

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is installed and running with your preferred model:
```bash
ollama pull llama3.2
```

## Usage

### Basic Single Agent Usage

```python
from orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(
    model_name="llama3.2",
    temperature=0.7,
    role_folder="Role"
)

backend_agent = orchestrator.get_agent("backend_developer")
response = backend_agent.chat("How should I design a microservices architecture?")
print(response)
```

### Using Specialized Methods

```python
backend_agent = orchestrator.get_agent("backend_developer")

code_review = backend_agent.review_code("""
def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
""", "python")

api_design = backend_agent.design_api("""
Create an API for a blog platform with posts, comments, and users.
Need CRUD operations for all entities.
""")
```

### Multi-Agent Consultation

```python
query = "We need to build a real-time chat application. What should we consider?"
agents = ["backend_developer", "frontend_developer", "devops_engineer"]

responses = orchestrator.multi_agent_consultation(query, agents)

for agent_name, response in responses.items():
    print(f"{agent_name}: {response}")
```

### Collaborative Workflow

```python
workflow = [
    {"agent": "product_manager", "action": "chat"},
    {"agent": "backend_developer", "action": "design_api"},
    {"agent": "qa_engineer", "action": "create_test_plan"}
]

task = "Build a payment processing system"
results = orchestrator.collaborative_task(task, workflow)
```

## Available Agents

1. **Backend Developer** (`backend_developer`)
   - `review_code(code, language)` - Code review and suggestions
   - `design_api(requirements)` - API design
   - `suggest_architecture(description)` - Architecture recommendations

2. **DevOps Engineer** (`devops_engineer`)
   - `create_ci_cd_pipeline(project_info)` - CI/CD pipeline design
   - `review_infrastructure(description)` - Infrastructure review
   - `troubleshoot_deployment(issue)` - Deployment troubleshooting
   - `design_monitoring(system)` - Monitoring strategy

3. **Product Manager** (`product_manager`)
   - `create_product_roadmap(vision)` - Product roadmap creation
   - `write_user_stories(feature)` - User story writing
   - `analyze_market(idea)` - Market analysis
   - `prioritize_features(features)` - Feature prioritization

4. **QA Engineer** (`qa_engineer`)
   - `create_test_plan(feature)` - Test plan creation
   - `review_test_coverage(suite)` - Test coverage review
   - `create_automation_strategy(project)` - Automation strategy
   - `analyze_bug_report(bug)` - Bug analysis

5. **Frontend Developer** (`frontend_developer`)
   - `review_ui_code(code, framework)` - UI code review
   - `design_component_architecture(requirements)` - Component design
   - `optimize_performance(issue)` - Performance optimization
   - `implement_responsive_design(requirements)` - Responsive design

6. **Data Engineer** (`data_engineer`)
   - `design_data_pipeline(requirements)` - Data pipeline design
   - `optimize_query(query, context)` - Query optimization
   - `design_data_warehouse(requirements)` - Data warehouse design
   - `troubleshoot_pipeline(issue)` - Pipeline troubleshooting

## Running the Example

```bash
python main.py
```

This will demonstrate:
- Single agent interaction
- Multi-agent consultation
- Collaborative workflows
- Specialized agent methods

## Customization

### Adding New Agents

1. Create a new folder under `agents/` (e.g., `agents/security_engineer/`)
2. Create `agent.py` with a class inheriting from `BaseAgent`
3. Specify the role file from the `Role` folder
4. Add specialized methods as needed
5. Register the agent in `orchestrator.py`

Example:
```python
class SecurityEngineerAgent(BaseAgent):
    def __init__(self, model_name="llama3.2", temperature=0.7, role_folder="Role"):
        super().__init__(
            role_filename="Security_Engineer.txt",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
    
    def security_audit(self, code):
        prompt = f"Perform a security audit on: {code}"
        return self.chat(prompt)
```

### Changing LLM Model

```python
orchestrator = AgentOrchestrator(
    model_name="mistral",  # or any other Ollama model
    temperature=0.5
)
```

## Notes

- Each agent maintains its own conversation history
- Use `clear_agent_memory(agent_name)` to reset a specific agent
- Use `clear_all_memories()` to reset all agents
- Role definitions are loaded from the `Role` folder at initialization
- Agents automatically parse role metadata (title, level, department, experience)
