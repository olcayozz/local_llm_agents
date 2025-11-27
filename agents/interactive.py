import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from orchestrator import AgentOrchestrator

def interactive_mode():
    print("=" * 70)
    print("Interactive Multi-Agent System")
    print("=" * 70)
    
    orchestrator = AgentOrchestrator(
        model_name="llama3.2",
        temperature=0.7,
        role_folder="Role"
    )
    
    print("\nAvailable Agents:")
    agents = orchestrator.list_agents()
    for i, agent_name in enumerate(agents, 1):
        info = orchestrator.get_agent_info(agent_name)
        print(f"  {i}. {agent_name.replace('_', ' ').title()}")
    
    print("\nCommands:")
    print("  - Type agent name to select an agent")
    print("  - Type 'list' to see available agents")
    print("  - Type 'switch' to change agent")
    print("  - Type 'clear' to clear current agent memory")
    print("  - Type 'multi' for multi-agent consultation")
    print("  - Type 'exit' to quit")
    print("=" * 70)
    
    current_agent = None
    current_agent_name = None
    
    while True:
        if current_agent_name:
            prompt = f"\n[{current_agent_name}] > "
        else:
            prompt = "\n[Select Agent] > "
        
        user_input = input(prompt).strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'exit':
            print("\nGoodbye!")
            break
        
        elif user_input.lower() == 'list':
            print("\nAvailable Agents:")
            for i, agent_name in enumerate(agents, 1):
                print(f"  {i}. {agent_name.replace('_', ' ').title()}")
        
        elif user_input.lower() == 'switch':
            current_agent = None
            current_agent_name = None
            print("\nAgent deselected. Choose a new agent.")
        
        elif user_input.lower() == 'clear':
            if current_agent:
                current_agent.clear_memory()
                print(f"\nMemory cleared for {current_agent_name}")
            else:
                print("\nNo agent selected.")
        
        elif user_input.lower() == 'multi':
            print("\nEnter agent names separated by commas (e.g., backend_developer, devops_engineer):")
            agent_input = input("> ").strip()
            selected_agents = [a.strip() for a in agent_input.split(',')]
            
            print("\nEnter your query:")
            query = input("> ").strip()
            
            if query:
                print("\nConsulting agents...\n")
                responses = orchestrator.multi_agent_consultation(query, selected_agents)
                
                for agent_name, response in responses.items():
                    print(f"\n{'=' * 70}")
                    print(f"{agent_name.replace('_', ' ').title()}:")
                    print(f"{'=' * 70}")
                    print(response)
        
        elif user_input.lower() in agents:
            current_agent_name = user_input.lower()
            current_agent = orchestrator.get_agent(current_agent_name)
            info = orchestrator.get_agent_info(current_agent_name)
            print(f"\nSelected: {info.get('title', current_agent_name)}")
            print(f"Level: {info.get('level', 'N/A')}")
            print(f"Department: {info.get('department', 'N/A')}")
        
        else:
            if current_agent:
                print("\nThinking...")
                response = current_agent.chat(user_input)
                print(f"\n{response}")
            else:
                print("\nPlease select an agent first. Type 'list' to see available agents.")

if __name__ == "__main__":
    interactive_mode()
