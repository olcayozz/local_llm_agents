from typing import Literal
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
import os
import json

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "websearch", "ask"] = Field(
        ...,
        description="Given a user question choose to route it to vectorstore, websearch, ask. Only these three options are valid. If you are unsure, keep asking the human until you decide. RESPOND ONLY ONE WORD. Re-check if answer is one word or not. It has to be one word.",
    )


def transform_output(text: str) -> str:
    cleaned_text = text.strip().lower()
    return json.dumps({"datasource": cleaned_text})


parser = PydanticOutputParser(pydantic_object=RouteQuery)


def route_function(question: str) -> RouteQuery:
    
    if question["question"].startswith("SCKS"):
        return RouteQuery(datasource="vectorstore")
    return RouteQuery(datasource="websearch")

# Convert to Runnable
route_runnable = RunnableLambda(route_function)


question_router = route_runnable