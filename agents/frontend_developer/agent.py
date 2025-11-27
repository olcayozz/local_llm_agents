import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.base_agent import BaseAgent

class FrontendDeveloperAgent(BaseAgent):
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        super().__init__(
            role_filename="Software_Developer_Frontend.txt",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
    
    def review_ui_code(self, code: str, framework: str = "React") -> str:
        prompt = f"""As a Frontend Developer, review this {framework} code:

{code}

Please analyze:
1. Component structure and reusability
2. State management approach
3. Performance optimizations
4. Accessibility (a11y) compliance
5. Best practices and improvements
"""
        return self.chat(prompt)
    
    def design_component_architecture(self, requirements: str) -> str:
        prompt = f"""As a Frontend Developer, design a component architecture for:

{requirements}

Please provide:
1. Component hierarchy
2. Props and state management
3. Reusable components identification
4. Styling approach
5. Performance considerations
"""
        return self.chat(prompt)
    
    def optimize_performance(self, performance_issue: str) -> str:
        prompt = f"""As a Frontend Developer, help optimize this performance issue:

{performance_issue}

Please suggest:
1. Performance bottleneck analysis
2. Optimization techniques
3. Code splitting strategies
4. Lazy loading opportunities
5. Caching strategies
"""
        return self.chat(prompt)
    
    def implement_responsive_design(self, design_requirements: str) -> str:
        prompt = f"""As a Frontend Developer, create a responsive design strategy for:

{design_requirements}

Please include:
1. Breakpoint strategy
2. Mobile-first vs. desktop-first approach
3. CSS framework recommendations
4. Testing approach for different devices
5. Progressive enhancement strategy
"""
        return self.chat(prompt)
