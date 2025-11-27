import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.base_agent import BaseAgent

class DataEngineerAgent(BaseAgent):
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        super().__init__(
            role_filename="Data_Engineer.txt",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
    
    def design_data_pipeline(self, requirements: str) -> str:
        prompt = f"""As a Data Engineer, design a data pipeline for:

{requirements}

Please provide:
1. Data sources and ingestion methods
2. ETL/ELT process design
3. Data transformation logic
4. Storage solutions
5. Monitoring and error handling
"""
        return self.chat(prompt)
    
    def optimize_query(self, query: str, context: str = "") -> str:
        prompt = f"""As a Data Engineer, optimize this database query:

Query:
{query}

Context:
{context}

Please provide:
1. Performance analysis
2. Optimized query version
3. Index recommendations
4. Execution plan insights
5. Best practices applied
"""
        return self.chat(prompt)
    
    def design_data_warehouse(self, business_requirements: str) -> str:
        prompt = f"""As a Data Engineer, design a data warehouse for:

{business_requirements}

Please include:
1. Schema design (star/snowflake)
2. Dimension and fact tables
3. Data modeling approach
4. ETL strategy
5. Technology stack recommendations
"""
        return self.chat(prompt)
    
    def troubleshoot_pipeline(self, issue_description: str) -> str:
        prompt = f"""As a Data Engineer, troubleshoot this data pipeline issue:

{issue_description}

Please provide:
1. Root cause analysis
2. Diagnostic steps
3. Solution recommendations
4. Data quality checks
5. Prevention measures
"""
        return self.chat(prompt)
