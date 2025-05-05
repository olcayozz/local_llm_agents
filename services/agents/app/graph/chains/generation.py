from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
        base_url="http://ollama:11434",
        model="smollm2",
        temperature=0,
    )
prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()
