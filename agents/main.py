import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from orchestrator import AgentOrchestrator

def main():
    print("=" * 60)
    print("Multi-Agent System - LangChain with Role-Based Agents")
    print("=" * 60)
    
    orchestrator = AgentOrchestrator(
        model_name="llama3.2",
        temperature=0.7,
        role_folder="Role"
    )
    
    print("\nAvailable Agents:")
    for i, agent_name in enumerate(orchestrator.list_agents(), 1):
        info = orchestrator.get_agent_info(agent_name)
        print(f"{i}. {agent_name}: {info.get('title', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("Example 1: Single Agent Interaction")
    print("=" * 60)
    
    backend_agent = orchestrator.get_agent("backend_developer")
    response = backend_agent.chat("What are the best practices for designing a RESTful API?")
    print(f"\nBackend Developer Response:\n{response[:500]}...")
    
    print("\n" + "=" * 60)
    print("Example 2: Multi-Agent Consultation")
    print("=" * 60)
    
    query = "We need to build a scalable e-commerce platform. What should we consider?"
    agents_to_consult = ["product_manager", "backend_developer", "devops_engineer"]
    
    responses = orchestrator.multi_agent_consultation(query, agents_to_consult)
    
    for agent_name, response in responses.items():
        print(f"\n{agent_name.upper()}:")
        print(f"{response[:300]}...")
    
    print("\n" + "=" * 60)
    print("Example 3: Collaborative Workflow")
    print("=" * 60)
    
    workflow = [
        {"agent": "product_manager", "action": "chat"},
        {"agent": "backend_developer", "action": "chat"},
        {"agent": "qa_engineer", "action": "chat"}
    ]
    
    task = "Design a user authentication system with OAuth2"
    results = orchestrator.collaborative_task(task, workflow)
    
    for result in results:
        print(f"\n{result['agent'].upper()} - {result['action']}:")
        print(f"{result['response'][:300]}...")
    
    print("\n" + "=" * 60)
    print("Example 4: Specialized Agent Methods")
    print("=" * 60)
    
    backend_agent = orchestrator.get_agent("backend_developer")
    code_review = backend_agent.review_code("""
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price']
    return total
""", "python")
    
    print(f"\nCode Review:\n{code_review[:400]}...")
    
    orchestrator.clear_all_memories()
    print("\n\nAll agent memories cleared.")

if __name__ == "__main__":
    main()
