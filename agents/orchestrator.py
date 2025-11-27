from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from backend_developer.agent import BackendDeveloperAgent
from devops_engineer.agent import DevOpsEngineerAgent
from product_manager.agent import ProductManagerAgent
from qa_engineer.agent import QAEngineerAgent
from frontend_developer.agent import FrontendDeveloperAgent
from data_engineer.agent import DataEngineerAgent
from project_manager.agent import ProjectManagerAgent
from scrum_master.agent import ScrumMasterAgent
from fullstack_developer.agent import FullStackDeveloperAgent
from mobile_developer_android.agent import MobileDeveloperAndroidAgent
from mobile_developer_ios.agent import MobileDeveloperIOSAgent
from security_engineer.agent import SecurityEngineerAgent
from site_reliability_engineer.agent import SiteReliabilityEngineerAgent
from database_administrator.agent import DatabaseAdministratorAgent
from data_analyst.agent import DataAnalystAgent
from business_intelligence_analyst.agent import BusinessIntelligenceAnalystAgent
from cloud_architect.agent import CloudArchitectAgent
from solutions_architect.agent import SolutionsArchitectAgent
from network_engineer.agent import NetworkEngineerAgent
from system_administrator.agent import SystemAdministratorAgent
from it_support_l1.agent import ITSupportL1Agent
from it_support_l2.agent import ITSupportL2Agent
from it_support_l3.agent import ITSupportL3Agent
from engineering_manager.agent import EngineeringManagerAgent
from devops_manager.agent import DevOpsManagerAgent
from it_manager.agent import ITManagerAgent
from cto.agent import CTOAgent
from ui_ux_designer.agent import UIUXDesignerAgent
from technical_writer.agent import TechnicalWriterAgent
from utils.meeting import Meeting, MeetingType, MeetingParticipantSelector

class AgentOrchestrator:
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        self.agents: Dict[str, Any] = {}
        self.model_name = model_name
        self.temperature = temperature
        self.role_folder = role_folder
        self.meetings: List[Meeting] = []

        self._initialize_agents()
    
    def _initialize_agents(self):
        self.agents = {
            "backend_developer": BackendDeveloperAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "frontend_developer": FrontendDeveloperAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "fullstack_developer": FullStackDeveloperAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "mobile_developer_android": MobileDeveloperAndroidAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "mobile_developer_ios": MobileDeveloperIOSAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "devops_engineer": DevOpsEngineerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "devops_manager": DevOpsManagerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "site_reliability_engineer": SiteReliabilityEngineerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "security_engineer": SecurityEngineerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "product_manager": ProductManagerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "project_manager": ProjectManagerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "scrum_master": ScrumMasterAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "engineering_manager": EngineeringManagerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "it_manager": ITManagerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "cto": CTOAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "qa_engineer": QAEngineerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "data_engineer": DataEngineerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "data_analyst": DataAnalystAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "business_intelligence_analyst": BusinessIntelligenceAnalystAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "database_administrator": DatabaseAdministratorAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "cloud_architect": CloudArchitectAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "solutions_architect": SolutionsArchitectAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "network_engineer": NetworkEngineerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "system_administrator": SystemAdministratorAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "it_support_l1": ITSupportL1Agent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "it_support_l2": ITSupportL2Agent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "it_support_l3": ITSupportL3Agent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "ui_ux_designer": UIUXDesignerAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            ),
            "technical_writer": TechnicalWriterAgent(
                model_name=self.model_name,
                temperature=self.temperature,
                role_folder=self.role_folder
            )
        }
    
    def get_agent(self, agent_name: str):
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found. Available agents: {list(self.agents.keys())}")
        return self.agents[agent_name]
    
    def list_agents(self) -> List[str]:
        return list(self.agents.keys())
    
    def get_agent_info(self, agent_name: str) -> Dict[str, str]:
        agent = self.get_agent(agent_name)
        return agent.get_role_info()
    
    def chat_with_agent(self, agent_name: str, message: str) -> str:
        agent = self.get_agent(agent_name)
        return agent.chat(message)
    
    def multi_agent_consultation(
        self,
        query: str,
        agent_names: List[str]
    ) -> Dict[str, str]:
        responses = {}
        
        for agent_name in agent_names:
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                responses[agent_name] = agent.chat(query)
        
        return responses
    
    def collaborative_task(
        self,
        task_description: str,
        workflow: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        results = []
        context = task_description
        
        for step in workflow:
            agent_name = step.get("agent")
            action = step.get("action", "chat")
            
            if agent_name not in self.agents:
                results.append({
                    "agent": agent_name,
                    "error": f"Agent not found: {agent_name}"
                })
                continue
            
            agent = self.agents[agent_name]
            
            if action == "chat":
                response = agent.chat(context)
            else:
                method = getattr(agent, action, None)
                if method and callable(method):
                    response = method(context)
                else:
                    response = agent.chat(context)
            
            results.append({
                "agent": agent_name,
                "action": action,
                "response": response
            })
            
            context = f"{context}\n\nPrevious response from {agent_name}:\n{response}"
        
        return results
    
    def clear_all_memories(self):
        for agent in self.agents.values():
            agent.clear_memory()
    
    def clear_agent_memory(self, agent_name: str):
        agent = self.get_agent(agent_name)
        agent.clear_memory()
