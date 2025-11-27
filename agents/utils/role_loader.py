import os
from pathlib import Path
from typing import Dict, Optional

class RoleLoader:
    def __init__(self, role_folder: str = "Role"):
        self.role_folder = Path(role_folder)
        if not self.role_folder.exists():
            raise FileNotFoundError(f"Role folder not found: {role_folder}")
    
    def load_role(self, role_filename: str) -> str:
        role_path = self.role_folder / role_filename
        if not role_path.exists():
            raise FileNotFoundError(f"Role file not found: {role_path}")
        
        with open(role_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    
    def get_role_prompt(self, role_filename: str) -> str:
        role_content = self.load_role(role_filename)
        
        prompt = f"""You are an AI agent acting as the role defined below. Follow all the guidelines, responsibilities, and expertise areas mentioned in your role definition.

{role_content}

Based on this role definition, respond to user queries with the expertise, knowledge, and perspective of this role. Apply the skills, tools, and methodologies mentioned in your role description."""
        
        return prompt
    
    def list_available_roles(self) -> list:
        return [f.name for f in self.role_folder.glob("*.txt")]
    
    def get_role_metadata(self, role_filename: str) -> Dict[str, str]:
        content = self.load_role(role_filename)
        lines = content.split('\n')
        
        metadata = {
            'title': '',
            'level': '',
            'department': '',
            'experience': ''
        }
        
        for line in lines[:20]:
            if line.startswith('#') and not line.startswith('##'):
                metadata['title'] = line.strip('# ').strip()
            elif 'Pozisyon Seviyesi:' in line:
                metadata['level'] = line.split(':', 1)[1].strip().strip('*')
            elif 'Departman:' in line:
                metadata['department'] = line.split(':', 1)[1].strip().strip('*')
            elif 'Deneyim Gereksinimi:' in line:
                metadata['experience'] = line.split(':', 1)[1].strip().strip('*')
        
        return metadata
