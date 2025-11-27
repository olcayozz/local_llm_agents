"""
Script to generate all missing agent files based on Role folder
"""
from pathlib import Path

# Mapping of role files to agent folder names and class names
AGENT_MAPPINGS = [
    ("Project_Manager.txt", "project_manager", "ProjectManagerAgent"),
    ("Scrum_Master.txt", "scrum_master", "ScrumMasterAgent"),
    ("Software_Developer_FullStack.txt", "fullstack_developer", "FullStackDeveloperAgent"),
    ("Mobile_Developer_Android.txt", "mobile_developer_android", "MobileDeveloperAndroidAgent"),
    ("Mobile_Developer_iOS.txt", "mobile_developer_ios", "MobileDeveloperIOSAgent"),
    ("Security_Engineer.txt", "security_engineer", "SecurityEngineerAgent"),
    ("Site_Reliability_Engineer.txt", "site_reliability_engineer", "SiteReliabilityEngineerAgent"),
    ("Database_Administrator.txt", "database_administrator", "DatabaseAdministratorAgent"),
    ("Data_Analyst.txt", "data_analyst", "DataAnalystAgent"),
    ("Business_Intelligence_Analyst.txt", "business_intelligence_analyst", "BusinessIntelligenceAnalystAgent"),
    ("Cloud_Architect.txt", "cloud_architect", "CloudArchitectAgent"),
    ("Solutions_Architect.txt", "solutions_architect", "SolutionsArchitectAgent"),
    ("Network_Engineer.txt", "network_engineer", "NetworkEngineerAgent"),
    ("System_Administrator.txt", "system_administrator", "SystemAdministratorAgent"),
    ("IT_Support_L1.txt", "it_support_l1", "ITSupportL1Agent"),
    ("IT_Support_L2.txt", "it_support_l2", "ITSupportL2Agent"),
    ("IT_Support_L3.txt", "it_support_l3", "ITSupportL3Agent"),
    ("Engineering_Manager.txt", "engineering_manager", "EngineeringManagerAgent"),
    ("DevOps_Manager.txt", "devops_manager", "DevOpsManagerAgent"),
    ("IT_Manager_Director.txt", "it_manager", "ITManagerAgent"),
    ("CTO_CIO.txt", "cto", "CTOAgent"),
    ("UI_UX_Designer.txt", "ui_ux_designer", "UIUXDesignerAgent"),
    ("Technical_Writer.txt", "technical_writer", "TechnicalWriterAgent"),
]

AGENT_TEMPLATE = '''import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.base_agent import BaseAgent

class {class_name}(BaseAgent):
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        super().__init__(
            role_filename="{role_filename}",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
'''

INIT_TEMPLATE = '''from .agent import {class_name}

__all__ = ['{class_name}']
'''

def create_agent_files():
    agents_dir = Path("agents")
    
    for role_filename, folder_name, class_name in AGENT_MAPPINGS:
        agent_dir = agents_dir / folder_name
        agent_dir.mkdir(exist_ok=True)
        
        # Create agent.py
        agent_file = agent_dir / "agent.py"
        agent_content = AGENT_TEMPLATE.format(
            class_name=class_name,
            role_filename=role_filename
        )
        agent_file.write_text(agent_content)
        print(f"✓ Created {agent_file}")
        
        # Create __init__.py
        init_file = agent_dir / "__init__.py"
        init_content = INIT_TEMPLATE.format(class_name=class_name)
        init_file.write_text(init_content)
        print(f"✓ Created {init_file}")

if __name__ == "__main__":
    print("Generating missing agent files...")
    create_agent_files()
    print("\nAll agent files created successfully!")
