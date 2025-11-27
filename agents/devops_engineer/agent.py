import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.base_agent import BaseAgent

class DevOpsEngineerAgent(BaseAgent):
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        super().__init__(
            role_filename="DevOps_Engineer.txt",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
    
    def create_ci_cd_pipeline(self, project_info: str) -> str:
        prompt = f"""As a DevOps Engineer, design a CI/CD pipeline for this project:

{project_info}

Please provide:
1. Pipeline stages (build, test, deploy)
2. Tools and technologies to use
3. Deployment strategy
4. Rollback procedures
5. Monitoring and alerting setup
"""
        return self.chat(prompt)
    
    def review_infrastructure(self, infrastructure_description: str) -> str:
        prompt = f"""As a DevOps Engineer, review this infrastructure setup:

{infrastructure_description}

Please analyze:
1. Security vulnerabilities
2. Scalability issues
3. Cost optimization opportunities
4. High availability considerations
5. Disaster recovery readiness
"""
        return self.chat(prompt)
    
    def troubleshoot_deployment(self, issue_description: str) -> str:
        prompt = f"""As a DevOps Engineer, help troubleshoot this deployment issue:

{issue_description}

Please provide:
1. Possible root causes
2. Diagnostic steps
3. Solution recommendations
4. Prevention strategies
"""
        return self.chat(prompt)
    
    def design_monitoring(self, system_description: str) -> str:
        prompt = f"""As a DevOps Engineer, design a monitoring and observability solution for:

{system_description}

Please include:
1. Metrics to monitor
2. Logging strategy
3. Alerting rules
4. Dashboard recommendations
5. Tools and technologies
"""
        return self.chat(prompt)
