import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.base_agent import BaseAgent

class UIUXDesignerAgent(BaseAgent):
    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        super().__init__(
            role_filename="UI_UX_Designer.txt",
            model_name=model_name,
            temperature=temperature,
            role_folder=role_folder
        )
