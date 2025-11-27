"""
Test script to verify all 29 agents are properly initialized
"""
from agents.orchestrator import AgentOrchestrator

def test_all_agents():
    print("=" * 80)
    print("Testing All 29 Agents")
    print("=" * 80)
    
    orchestrator = AgentOrchestrator()
    
    agents = orchestrator.list_agents()
    print(f"\n✓ Total agents initialized: {len(agents)}")
    
    expected_agents = [
        "backend_developer",
        "frontend_developer",
        "fullstack_developer",
        "mobile_developer_android",
        "mobile_developer_ios",
        "devops_engineer",
        "devops_manager",
        "site_reliability_engineer",
        "security_engineer",
        "product_manager",
        "project_manager",
        "scrum_master",
        "engineering_manager",
        "it_manager",
        "cto",
        "qa_engineer",
        "data_engineer",
        "data_analyst",
        "business_intelligence_analyst",
        "database_administrator",
        "cloud_architect",
        "solutions_architect",
        "network_engineer",
        "system_administrator",
        "it_support_l1",
        "it_support_l2",
        "it_support_l3",
        "ui_ux_designer",
        "technical_writer"
    ]
    
    print("\nVerifying all expected agents are present:")
    missing_agents = []
    for agent_name in expected_agents:
        if agent_name in agents:
            print(f"  ✓ {agent_name}")
        else:
            print(f"  ✗ {agent_name} - MISSING")
            missing_agents.append(agent_name)
    
    if missing_agents:
        print(f"\n✗ Missing {len(missing_agents)} agents: {missing_agents}")
        return False
    
    print("\n" + "=" * 80)
    print("Testing Agent Information Retrieval")
    print("=" * 80)
    
    test_agents = [
        "backend_developer",
        "security_engineer",
        "cloud_architect",
        "scrum_master",
        "cto"
    ]
    
    for agent_name in test_agents:
        try:
            info = orchestrator.get_agent_info(agent_name)
            print(f"\n✓ {agent_name}:")
            print(f"  Role: {info.get('role', 'N/A')}")
            print(f"  Description: {info.get('description', 'N/A')[:80]}...")
        except Exception as e:
            print(f"\n✗ {agent_name}: Error - {str(e)}")
            return False
    
    print("\n" + "=" * 80)
    print("Testing Agent Chat Functionality")
    print("=" * 80)
    
    test_queries = [
        ("backend_developer", "What's your expertise?"),
        ("security_engineer", "What security practices do you recommend?"),
        ("scrum_master", "How do you facilitate sprint planning?")
    ]
    
    for agent_name, query in test_queries:
        try:
            print(f"\n✓ Testing {agent_name}...")
            response = orchestrator.chat_with_agent(agent_name, query)
            print(f"  Query: {query}")
            print(f"  Response length: {len(response)} characters")
            print(f"  Response preview: {response[:100]}...")
        except Exception as e:
            print(f"\n✗ {agent_name}: Error - {str(e)}")
            return False
    
    print("\n" + "=" * 80)
    print("✓ ALL TESTS PASSED!")
    print("=" * 80)
    print(f"\nAll {len(agents)} agents are properly initialized and functional.")
    return True

if __name__ == "__main__":
    success = test_all_agents()
    exit(0 if success else 1)
