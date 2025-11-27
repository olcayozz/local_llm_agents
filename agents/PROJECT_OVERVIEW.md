# Multi-Agent LLM System - Project Overview

## 📋 Project Summary

A sophisticated multi-agent AI system built with LangChain where each agent acts according to specific professional roles defined in the `Role` folder. The system supports individual agent interactions, multi-agent consultations, and collaborative workflows.

## 🏗️ Architecture

### Core Components

1. **Role Loader** (`utils/role_loader.py`)
   - Loads role definitions from text files in the Role folder
   - Parses role metadata (title, level, department, experience)
   - Generates system prompts based on role content

2. **Base Agent** (`utils/base_agent.py`)
   - Abstract base class for all agents
   - Handles LLM initialization (Ollama)
   - Manages conversation memory
   - Provides common chat interface

3. **Specialized Agents** (6 agents in separate folders)
   - Backend Developer
   - DevOps Engineer
   - Product Manager
   - QA Engineer
   - Frontend Developer
   - Data Engineer

4. **Orchestrator** (`orchestrator.py`)
   - Manages all agents
   - Coordinates multi-agent interactions
   - Handles collaborative workflows
   - Memory management across agents

## 📁 Project Structure

```
agents/
├── utils/
│   ├── __init__.py
│   ├── role_loader.py          # Role file loader and parser
│   └── base_agent.py            # Base agent class
│
├── backend_developer/
│   ├── __init__.py
│   └── agent.py                 # Backend Developer agent
│
├── devops_engineer/
│   ├── __init__.py
│   └── agent.py                 # DevOps Engineer agent
│
├── product_manager/
│   ├── __init__.py
│   └── agent.py                 # Product Manager agent
│
├── qa_engineer/
│   ├── __init__.py
│   └── agent.py                 # QA Engineer agent
│
├── frontend_developer/
│   ├── __init__.py
│   └── agent.py                 # Frontend Developer agent
│
├── data_engineer/
│   ├── __init__.py
│   └── agent.py                 # Data Engineer agent
│
├── tests/
│   ├── test_role_loader.py     # Unit tests for role loader
│   └── test_orchestrator.py    # Unit tests for orchestrator
│
├── orchestrator.py              # Main orchestrator
├── main.py                      # Example usage
├── interactive.py               # Interactive CLI
├── demo.py                      # Comprehensive demos
├── requirements.txt             # Dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # Documentation
```

## 🎯 Key Features

### 1. Role-Based Behavior
- Each agent imports its behavior from a specific role file in the `Role` folder
- Role definitions include responsibilities, skills, tools, and expertise
- Agents respond according to their role's perspective and knowledge

### 2. Specialized Methods
Each agent has domain-specific methods:

**Backend Developer:**
- `review_code()` - Code review and suggestions
- `design_api()` - RESTful API design
- `suggest_architecture()` - Architecture recommendations

**DevOps Engineer:**
- `create_ci_cd_pipeline()` - CI/CD pipeline design
- `review_infrastructure()` - Infrastructure analysis
- `troubleshoot_deployment()` - Deployment issue resolution
- `design_monitoring()` - Monitoring strategy

**Product Manager:**
- `create_product_roadmap()` - Product roadmap creation
- `write_user_stories()` - User story writing
- `analyze_market()` - Market analysis
- `prioritize_features()` - Feature prioritization

**QA Engineer:**
- `create_test_plan()` - Test plan creation
- `review_test_coverage()` - Coverage analysis
- `create_automation_strategy()` - Test automation design
- `analyze_bug_report()` - Bug analysis

**Frontend Developer:**
- `review_ui_code()` - UI code review
- `design_component_architecture()` - Component design
- `optimize_performance()` - Performance optimization
- `implement_responsive_design()` - Responsive design strategy

**Data Engineer:**
- `design_data_pipeline()` - Data pipeline design
- `optimize_query()` - Query optimization
- `design_data_warehouse()` - Data warehouse design
- `troubleshoot_pipeline()` - Pipeline troubleshooting

### 3. Memory Management
- Each agent maintains its own conversation history
- Memory can be cleared per agent or globally
- Conversation history accessible for review

### 4. Multi-Agent Collaboration
- **Multi-Agent Consultation**: Get perspectives from multiple agents on the same query
- **Collaborative Workflows**: Chain agents together where each builds on previous responses
- **Context Passing**: Agents can share context in workflows

### 5. Flexible Integration
- Uses Ollama for local LLM execution
- Supports any Ollama-compatible model
- Configurable temperature and model parameters

## 🚀 Usage Examples

### Single Agent Interaction
```python
from orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(role_folder="Role")
backend = orchestrator.get_agent("backend_developer")

response = backend.chat("How should I design a microservices architecture?")
print(response)
```

### Specialized Method Usage
```python
code_review = backend.review_code("""
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price']
    return total
""", "python")
```

### Multi-Agent Consultation
```python
query = "We need to build a real-time chat application"
agents = ["backend_developer", "frontend_developer", "devops_engineer"]

responses = orchestrator.multi_agent_consultation(query, agents)
for agent, response in responses.items():
    print(f"{agent}: {response}")
```

### Collaborative Workflow
```python
workflow = [
    {"agent": "product_manager", "action": "write_user_stories"},
    {"agent": "backend_developer", "action": "design_api"},
    {"agent": "qa_engineer", "action": "create_test_plan"}
]

results = orchestrator.collaborative_task(
    "Build a payment processing system",
    workflow
)
```

## 🛠️ Running the System

### Prerequisites
1. Python 3.8+
2. Ollama installed and running
3. A model pulled in Ollama (e.g., `ollama pull llama3.2`)

### Installation
```bash
cd agents
pip install -r requirements.txt
```

### Run Examples
```bash
# Basic examples
python main.py

# Interactive mode
python interactive.py

# Comprehensive demos
python demo.py

# Run tests
python -m pytest tests/
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
TEMPERATURE=0.7
ROLE_FOLDER=Role
```

### Custom Model
```python
orchestrator = AgentOrchestrator(
    model_name="mistral",  # or any Ollama model
    temperature=0.5
)
```

## 📝 Adding New Agents

1. Create a new folder: `agents/new_agent/`
2. Create `agent.py`:
```python
from utils.base_agent import BaseAgent

class NewAgent(BaseAgent):
    def __init__(self, model_name="llama3.2", temperature=0.7, role_folder="Role"):
        super().__init__(
            role_filename="New_Role.txt",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
    
    def custom_method(self, input_data):
        prompt = f"Perform task: {input_data}"
        return self.chat(prompt)
```

3. Create `__init__.py`:
```python
from .agent import NewAgent
__all__ = ['NewAgent']
```

4. Register in `orchestrator.py`:
```python
from new_agent.agent import NewAgent

# In _initialize_agents():
self.agents["new_agent"] = NewAgent(...)
```

## 🧪 Testing

Unit tests are provided for core components:
```bash
# Test role loader
python -m unittest tests/test_role_loader.py

# Test orchestrator
python -m unittest tests/test_orchestrator.py

# Run all tests
python -m unittest discover tests/
```

## 📊 Role Files

The system reads role definitions from the `Role` folder. Each role file should contain:
- Role title and metadata
- Responsibilities and duties
- Required skills and expertise
- Tools and technologies
- Best practices and methodologies

Example structure:
```
# Role Title

## GENEL BİLGİLER
**Pozisyon Seviyesi:** Level
**Departman:** Department
**Deneyim Gereksinimi:** Experience

## GÖREVLER VE SORUMLULUKLAR
- Responsibility 1
- Responsibility 2
...
```

## 🔄 Workflow Patterns

### Pattern 1: Sequential Processing
```python
workflow = [
    {"agent": "product_manager", "action": "chat"},
    {"agent": "backend_developer", "action": "chat"},
    {"agent": "qa_engineer", "action": "chat"}
]
```

### Pattern 2: Specialized Methods
```python
workflow = [
    {"agent": "product_manager", "action": "write_user_stories"},
    {"agent": "backend_developer", "action": "design_api"},
    {"agent": "qa_engineer", "action": "create_test_plan"}
]
```

### Pattern 3: Parallel Consultation
```python
agents = ["backend_developer", "frontend_developer", "data_engineer"]
responses = orchestrator.multi_agent_consultation(query, agents)
```

## 🎓 Best Practices

1. **Clear Agent Selection**: Choose agents based on the task domain
2. **Context Management**: Clear memory when switching contexts
3. **Workflow Design**: Structure workflows logically (PM → Dev → QA)
4. **Prompt Engineering**: Provide clear, specific prompts to agents
5. **Memory Management**: Clear memories periodically to avoid context overflow
6. **Temperature Tuning**: Lower for factual tasks, higher for creative tasks

## 🔐 Security Considerations

- Role files should not contain sensitive information
- Validate all user inputs before passing to agents
- Monitor LLM outputs for sensitive data leakage
- Use appropriate temperature settings for production
- Implement rate limiting for API-like usage

## 📈 Performance Tips

1. **Model Selection**: Choose appropriate model size for your hardware
2. **Temperature**: Lower values (0.3-0.5) for faster, more deterministic responses
3. **Memory Management**: Clear memories regularly to reduce context size
4. **Batch Processing**: Use multi-agent consultation for parallel processing
5. **Caching**: Consider caching common queries

## 🤝 Contributing

To add new agents or improve existing ones:
1. Follow the existing agent structure
2. Add comprehensive docstrings
3. Include unit tests
4. Update documentation
5. Ensure role file exists in Role folder

## 📄 License

This project structure is designed for local LLM agent development and can be adapted for various use cases.

## 🆘 Troubleshooting

**Issue**: Agent not responding
- Check if Ollama is running: `ollama list`
- Verify model is pulled: `ollama pull llama3.2`

**Issue**: Role file not found
- Ensure Role folder path is correct
- Check role filename matches exactly (case-sensitive)

**Issue**: Memory errors
- Clear agent memories: `orchestrator.clear_all_memories()`
- Reduce conversation length
- Use smaller model

**Issue**: Slow responses
- Use smaller model (e.g., llama3.2 instead of llama3.2:70b)
- Lower temperature
- Reduce context length
