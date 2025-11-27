import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.base_agent import BaseAgent

class BackendDeveloperAgent(BaseAgent):
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        super().__init__(
            role_filename="Software_Developer_Backend.txt",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
    
    def review_code(self, code: str, language: str = "python") -> str:
        prompt = f"""As a Backend Developer, please review the following {language} code and provide feedback on:
1. Code quality and best practices
2. Performance considerations
3. Security issues
4. Potential bugs
5. Suggestions for improvement

Code:
```{language}
{code}
```
"""
        return self.chat(prompt)
    
    def design_api(self, requirements: str) -> str:
        prompt = f"""As a Backend Developer, please design a RESTful API based on these requirements:

{requirements}

Please provide:
1. API endpoints with HTTP methods
2. Request/Response formats
3. Authentication/Authorization approach
4. Database schema suggestions
5. Error handling strategy
"""
        return self.chat(prompt)
    
    def suggest_architecture(self, project_description: str) -> str:
        prompt = f"""As a Backend Developer, suggest a backend architecture for this project:

{project_description}

Please include:
1. Technology stack recommendations
2. Architecture pattern (MVC, Microservices, etc.)
3. Database choices
4. Caching strategy
5. Scalability considerations
"""
        return self.chat(prompt)
