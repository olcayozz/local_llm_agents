import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from orchestrator import AgentOrchestrator

def demo_backend_developer():
    print("\n" + "=" * 70)
    print("DEMO: Backend Developer Agent")
    print("=" * 70)
    
    orchestrator = AgentOrchestrator(role_folder="Role")
    backend = orchestrator.get_agent("backend_developer")
    
    print("\n1. Code Review:")
    code = """
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    result = db.execute(query)
    return result
"""
    response = backend.review_code(code, "python")
    print(response)
    
    print("\n2. API Design:")
    requirements = "Need an API for managing blog posts with CRUD operations"
    response = backend.design_api(requirements)
    print(response)

def demo_devops_engineer():
    print("\n" + "=" * 70)
    print("DEMO: DevOps Engineer Agent")
    print("=" * 70)
    
    orchestrator = AgentOrchestrator(role_folder="Role")
    devops = orchestrator.get_agent("devops_engineer")
    
    print("\n1. CI/CD Pipeline Design:")
    project = "Python Flask API with PostgreSQL database"
    response = devops.create_ci_cd_pipeline(project)
    print(response)
    
    print("\n2. Monitoring Strategy:")
    system = "Microservices architecture with 5 services"
    response = devops.design_monitoring(system)
    print(response)

def demo_product_manager():
    print("\n" + "=" * 70)
    print("DEMO: Product Manager Agent")
    print("=" * 70)
    
    orchestrator = AgentOrchestrator(role_folder="Role")
    pm = orchestrator.get_agent("product_manager")
    
    print("\n1. User Stories:")
    feature = "User authentication with email and password"
    response = pm.write_user_stories(feature)
    print(response)
    
    print("\n2. Feature Prioritization:")
    features = """
    - Dark mode
    - Push notifications
    - Social media sharing
    - Advanced search
    - User profiles
    """
    response = pm.prioritize_features(features)
    print(response)

def demo_qa_engineer():
    print("\n" + "=" * 70)
    print("DEMO: QA Engineer Agent")
    print("=" * 70)
    
    orchestrator = AgentOrchestrator(role_folder="Role")
    qa = orchestrator.get_agent("qa_engineer")
    
    print("\n1. Test Plan:")
    feature = "User login functionality with OAuth"
    response = qa.create_test_plan(feature)
    print(response)
    
    print("\n2. Automation Strategy:")
    project = "E-commerce web application with React frontend"
    response = qa.create_automation_strategy(project)
    print(response)

def demo_collaboration():
    print("\n" + "=" * 70)
    print("DEMO: Multi-Agent Collaboration")
    print("=" * 70)
    
    orchestrator = AgentOrchestrator(role_folder="Role")
    
    print("\nScenario: Building a new feature - Payment Integration")
    print("\nStep 1: Product Manager defines requirements")
    
    workflow = [
        {"agent": "product_manager", "action": "write_user_stories"},
        {"agent": "backend_developer", "action": "design_api"},
        {"agent": "qa_engineer", "action": "create_test_plan"},
        {"agent": "devops_engineer", "action": "create_ci_cd_pipeline"}
    ]
    
    task = "Integrate Stripe payment gateway for subscription payments"
    results = orchestrator.collaborative_task(task, workflow)
    
    for i, result in enumerate(results, 1):
        print(f"\n{'=' * 70}")
        print(f"Step {i}: {result['agent'].replace('_', ' ').title()}")
        print(f"{'=' * 70}")
        print(result['response'][:500] + "...")

def main():
    print("=" * 70)
    print("Multi-Agent System - Comprehensive Demos")
    print("=" * 70)
    
    demos = {
        "1": ("Backend Developer", demo_backend_developer),
        "2": ("DevOps Engineer", demo_devops_engineer),
        "3": ("Product Manager", demo_product_manager),
        "4": ("QA Engineer", demo_qa_engineer),
        "5": ("Multi-Agent Collaboration", demo_collaboration),
        "6": ("Run All Demos", None)
    }
    
    print("\nAvailable Demos:")
    for key, (name, _) in demos.items():
        print(f"  {key}. {name}")
    print("  0. Exit")
    
    while True:
        choice = input("\nSelect demo (0-6): ").strip()
        
        if choice == "0":
            print("\nGoodbye!")
            break
        elif choice == "6":
            for key in ["1", "2", "3", "4", "5"]:
                demos[key][1]()
            break
        elif choice in demos and demos[choice][1]:
            demos[choice][1]()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
