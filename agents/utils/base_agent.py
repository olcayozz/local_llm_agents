from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from typing import List, Dict, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.role_loader import RoleLoader

class BaseAgent:
    def __init__(
        self,
        role_filename: str,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        role_folder: str = "Role"
    ):
        self.role_filename = role_filename
        self.role_loader = RoleLoader(role_folder)
        self.role_prompt = self.role_loader.get_role_prompt(role_filename)
        self.role_metadata = self.role_loader.get_role_metadata(role_filename)
        
        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature
        )
        
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        
        self.system_message = SystemMessage(content=self.role_prompt)
    
    def get_role_info(self) -> Dict[str, str]:
        return self.role_metadata
    
    def chat(self, user_message: str) -> str:
        messages = [self.system_message]
        
        chat_history = self.memory.load_memory_variables({})
        if chat_history.get('chat_history'):
            messages.extend(chat_history['chat_history'])
        
        messages.append(HumanMessage(content=user_message))
        
        response = self.llm.invoke(messages)
        
        self.memory.save_context(
            {"input": user_message},
            {"output": response.content}
        )
        
        return response.content
    
    def clear_memory(self):
        self.memory.clear()
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        chat_history = self.memory.load_memory_variables({})
        history = []
        
        if chat_history.get('chat_history'):
            for msg in chat_history['chat_history']:
                if isinstance(msg, HumanMessage):
                    history.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    history.append({"role": "assistant", "content": msg.content})
        
        return history
