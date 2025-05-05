from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_ollama import OllamaLLM




class GradeAnswer(BaseModel):

    binary_score: bool = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

parser = PydanticOutputParser(pydantic_object=GradeAnswer)

llm = OllamaLLM(
        base_url="http://ollama:11434",
        model="smollm2",
        temperature=0,
    )

system = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader: RunnableSequence = answer_prompt | llm | parser
