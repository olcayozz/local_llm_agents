from abacusai import ApiClient
import os

ABACUS_API_KEY=os.environ.get("ABACUS_API_KEY")
if not ABACUS_API_KEY:
    raise ValueError("ABACUS_API_KEY environment variable is not set.")

ABACUS_PROJECT_NAME=os.environ.get("ABACUS_PROJECT_NAME")
if not ABACUS_PROJECT_NAME:
    raise ValueError("ABACUS_PROJECT_NAME environment variable is not set.")

ABACUS_MODEL_ID=os.environ.get("ABACUS_MODEL_ID")
if not ABACUS_MODEL_ID:
    raise ValueError("ABACUS_MODEL_ID environment variable is not set.")



client = ApiClient(api_key=ABACUS_API_KEY)


system_prompt = "ONLY SHORT ANSWERS."    
    
def AbacusLLM(
    prompt: str,
    max_tokens: int = 20,
    temperature: float = 0.1,
) -> str:
    """Call the Abacus.AI API to get a response for the given prompt."""
    response = client.evaluate_prompt(
        system_prompt=system_prompt,
        prompt=prompt,
        llm_name=ABACUS_MODEL_ID,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.content
    

prompt = "What is the capital of France?"

llm = AbacusLLM(
        llm_name=prompt,
        max_tokens=20,
        temperature=0.1
    )


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



if __name__ == "__main__":