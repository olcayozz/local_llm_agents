# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd agents
pip install -r requirements.txt
```

### Step 2: Install and Start Ollama
```bash
# Install Ollama from https://ollama.ai

# Pull a model
ollama pull llama3.2

# Verify it's running
ollama list
```

### Step 3: Run Your First Agent
```bash
python main.py
```

## 💡 Quick Examples

### Example 1: Chat with Backend Developer
```python
from orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(role_folder="Role")
backend = orchestrator.get_agent("backend_developer")

response = backend.chat("What are REST API best practices?")
print(response)
```

### Example 2: Get Code Review
```python
backend = orchestrator.get_agent("backend_developer")

review = backend.review_code("""
def login(username, password):
    query = "SELECT * FROM users WHERE username='" + username + "'"
    user = db.execute(query)
    if user and user.password == password:
        return True
    return False
""", "python")

print(review)
```

### Example 3: Multi-Agent Consultation
```python
query = "How to build a scalable microservices architecture?"
agents = ["backend_developer", "devops_engineer", "data_engineer"]

responses = orchestrator.multi_agent_consultation(query, agents)

for agent, response in responses.items():
    print(f"\n{agent}:\n{response}\n")
```

### Example 4: Interactive Mode
```bash
python interactive.py
```

Then:
1. Type an agent name (e.g., `backend_developer`)
2. Start chatting!
3. Type `switch` to change agents
4. Type `multi` for multi-agent consultation

## 📚 Available Agents

| Agent | Role File | Specialization |
|-------|-----------|----------------|
| `backend_developer` | Software_Developer_Backend.txt | API design, architecture, code review |
| `frontend_developer` | Software_Developer_Frontend.txt | UI/UX, components, performance |
| `devops_engineer` | DevOps_Engineer.txt | CI/CD, infrastructure, monitoring |
| `product_manager` | Product_Manager.txt | Roadmaps, user stories, prioritization |
| `qa_engineer` | QA_Test_Engineer.txt | Test plans, automation, quality |
| `data_engineer` | Data_Engineer.txt | Pipelines, warehouses, ETL |

## 🎯 Common Use Cases

### Use Case 1: Feature Development
```python
workflow = [
    {"agent": "product_manager", "action": "write_user_stories"},
    {"agent": "backend_developer", "action": "design_api"},
    {"agent": "frontend_developer", "action": "design_component_architecture"},
    {"agent": "qa_engineer", "action": "create_test_plan"}
]

results = orchestrator.collaborative_task(
    "Build a user profile management feature",
    workflow
)
```

### Use Case 2: Code Review
```python
backend = orchestrator.get_agent("backend_developer")
review = backend.review_code(your_code, "python")
```

### Use Case 3: Infrastructure Planning
```python
devops = orchestrator.get_agent("devops_engineer")
pipeline = devops.create_ci_cd_pipeline("Python Flask API with Docker")
monitoring = devops.design_monitoring("Microservices with 5 services")
```

### Use Case 4: Product Planning
```python
pm = orchestrator.get_agent("product_manager")
roadmap = pm.create_product_roadmap("Build a SaaS analytics platform")
priorities = pm.prioritize_features("Feature list here...")
```

## 🔧 Configuration

### Change Model
```python
orchestrator = AgentOrchestrator(
    model_name="mistral",  # or codellama, llama2, etc.
    temperature=0.7
)
```

### Adjust Temperature
- **0.1-0.3**: Factual, deterministic (code review, analysis)
- **0.5-0.7**: Balanced (general chat, recommendations)
- **0.8-1.0**: Creative (brainstorming, ideation)

## 📝 Tips

1. **Be Specific**: Clear prompts get better responses
2. **Use Specialized Methods**: They're optimized for specific tasks
3. **Clear Memory**: Use `agent.clear_memory()` when switching contexts
4. **Chain Agents**: Use workflows for complex multi-step tasks
5. **Experiment**: Try different agents for different perspectives

## 🆘 Troubleshooting

**Problem**: "Role file not found"
- **Solution**: Make sure you're running from the project root and Role folder exists

**Problem**: "Connection refused"
- **Solution**: Start Ollama: `ollama serve`

**Problem**: Slow responses
- **Solution**: Use a smaller model or reduce temperature

**Problem**: Out of memory
- **Solution**: Clear agent memories or use a smaller model

## 📖 Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Check [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for architecture details
3. Run [demo.py](demo.py) to see all features
4. Explore [interactive.py](interactive.py) for hands-on experience

## 🎓 Learning Path

1. **Beginner**: Run `main.py` and `interactive.py`
2. **Intermediate**: Try specialized methods and multi-agent consultation
3. **Advanced**: Create collaborative workflows and add custom agents

Happy coding! 🚀
