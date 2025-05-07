from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
import os
import json



class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "websearch", "ask"] = Field(
        ...,
        description="Given a user question choose to route it to vectorstore, websearch, ask. Only these three options are valid. If you are unsure, keep asking the human until you decide. RESPOND ONLY ONE WORD. Re-check if answer is one word or not. It has to be one word.",
    )


llm = OllamaLLM(
        base_url=os.environ.get("OLLAMA_BASE_URL"),
        model=os.environ.get("OLLAMA_MODEL"),
        temperature=0,
    )


def transform_output(text: str) -> str:
    cleaned_text = text.strip().lower()
    return json.dumps({"datasource": cleaned_text})

parser = PydanticOutputParser(pydantic_object=RouteQuery)
str_parser = StrOutputParser()


system = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains SCKS related more spesific information. IF THE QUESTION IS START with SCKS then it is the answer must be 'vectorstore'.,
otherwise it is the answer must be 'websearch'.
THE ONLY ANSWER MUST BE EITHER 'vectorstore' OR 'websearch'. RESPOND ONLY ONE WORD. As a answer choose ONLY ONE OF 'vectorstore' OR 'websearch'."""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

llm_response= route_prompt | llm | (lambda x: transform_output(x))  # Convert to JSON format
#print("llm_response", llm_response)
llm_parsed_response = llm_response  | parser
#print("llm_parsed_response", llm_parsed_response)
question_router = llm_parsed_response