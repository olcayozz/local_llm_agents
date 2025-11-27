import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.base_agent import BaseAgent

class ProductManagerAgent(BaseAgent):
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        super().__init__(
            role_filename="Product_Manager.txt",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
    
    def create_product_roadmap(self, product_vision: str) -> str:
        prompt = f"""As a Product Manager, create a product roadmap based on this vision:

{product_vision}

Please provide:
1. Quarterly milestones
2. Feature prioritization
3. Success metrics (KPIs)
4. Resource requirements
5. Risk assessment
"""
        return self.chat(prompt)
    
    def write_user_stories(self, feature_description: str) -> str:
        prompt = f"""As a Product Manager, write user stories for this feature:

{feature_description}

Please provide:
1. User stories in standard format (As a... I want... So that...)
2. Acceptance criteria for each story
3. Priority levels
4. Story points estimation
5. Dependencies
"""
        return self.chat(prompt)
    
    def analyze_market(self, product_idea: str) -> str:
        prompt = f"""As a Product Manager, analyze the market for this product idea:

{product_idea}

Please provide:
1. Target market analysis
2. Competitive landscape
3. Market opportunities and threats
4. Product-market fit assessment
5. Go-to-market strategy recommendations
"""
        return self.chat(prompt)
    
    def prioritize_features(self, features_list: str) -> str:
        prompt = f"""As a Product Manager, prioritize these features:

{features_list}

Please use frameworks like RICE or MoSCoW and provide:
1. Prioritized feature list with rationale
2. Impact vs. effort analysis
3. Dependencies between features
4. Recommended release phases
"""
        return self.chat(prompt)
