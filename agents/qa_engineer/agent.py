import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.base_agent import BaseAgent

class QAEngineerAgent(BaseAgent):
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        super().__init__(
            role_filename="QA_Test_Engineer.txt",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
    
    def create_test_plan(self, feature_description: str) -> str:
        prompt = f"""As a QA Test Engineer, create a comprehensive test plan for:

{feature_description}

Please provide:
1. Test scope and objectives
2. Test cases (functional, non-functional)
3. Test data requirements
4. Testing tools and environment
5. Entry and exit criteria
"""
        return self.chat(prompt)
    
    def review_test_coverage(self, test_suite_description: str) -> str:
        prompt = f"""As a QA Test Engineer, review this test suite:

{test_suite_description}

Please analyze:
1. Coverage gaps
2. Missing test scenarios
3. Test redundancy
4. Test quality and maintainability
5. Recommendations for improvement
"""
        return self.chat(prompt)
    
    def create_automation_strategy(self, project_info: str) -> str:
        prompt = f"""As a QA Test Engineer, design a test automation strategy for:

{project_info}

Please include:
1. Automation framework selection
2. Test cases suitable for automation
3. Tools and technologies
4. CI/CD integration approach
5. Maintenance strategy
"""
        return self.chat(prompt)
    
    def analyze_bug_report(self, bug_description: str) -> str:
        prompt = f"""As a QA Test Engineer, analyze this bug report:

{bug_description}

Please provide:
1. Bug severity and priority assessment
2. Steps to reproduce (if missing)
3. Expected vs. actual behavior
4. Potential root cause
5. Regression testing recommendations
"""
        return self.chat(prompt)
