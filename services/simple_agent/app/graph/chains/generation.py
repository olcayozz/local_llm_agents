from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
from graph.chains.abacus_ai_wrapper import AbacusAILLM
import os

LOCAL_LLM = os.environ.get("LOCAL_LLM", "false")
llm=None

if LOCAL_LLM.lower() == "true": 
    llm = OllamaLLM(
            base_url=os.environ.get("OLLAMA_BASE_URL"),
            model=os.environ.get("OLLAMA_MODEL"),
            temperature=0,
        )
else:
    llm = AbacusAILLM()


system_prompt = "ONLY SHORT ANSWERS."

prompt =  hub.pull("rlm/rag-prompt")


template = """
{system_instructions}

{rag_prompt}
"""

prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_prompt),
    *prompt.messages
])

generation_chain = prompt_template | llm | StrOutputParser()