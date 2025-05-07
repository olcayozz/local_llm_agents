from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from abacusai import ApiClient
from pydantic import Field, PrivateAttr
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


class AbacusAILLM(LLM):
    """Wrapper around Abacus.AI large language models using official API client."""

    api_key: str = Field(default=ABACUS_API_KEY, description="Abacus.AI API key", )
    model_name: str = Field(default=ABACUS_MODEL_ID, description="Model name to use")
    temperature: float = Field(default=0.0, description="Sampling temperature")
    max_tokens: int = Field(default=50, description="Maximum number of tokens to generate")

    # Private attributes
    _client: ApiClient = ApiClient(api_key=ABACUS_API_KEY)

    def __init__(self, **kwargs):
        """Initialize the Abacus.AI LLM wrapper."""
        super().__init__(**kwargs)
        self._client = ApiClient(self.api_key)

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "abacus_ai"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """Execute the call to Abacus.AI using the API client."""
        try:
            response = self._client.evaluate_prompt(
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stop_sequences=stop if stop else None
            )

            return response.content

        except Exception as e:
            raise Exception(f"Error calling Abacus.AI API: {str(e)}")

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

# Example usage and utility functions
def create_abacusai_chain(api_key: str):
    """Create an abacusai LangChain chain using AbacusAILLM.

    Args:
        api_key (str): Your Abacus.AI API key

    Returns:
        LLMChain: A configured LangChain chain
    """
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate

    # Initialize the LLM
    llm = AbacusAILLM(api_key=api_key)

    # Create a prompt template
    template = """Question: {question}

    Please provide a detailed answer:"""

    prompt = PromptTemplate(
        input_variables=["question"],
        template=template
    )

    # Create and return the chain
    return prompt | llm


"""def example_usage():

    # Replace with your actual API key
    API_KEY = ABACUS_API_KEY

    # Basic LLM usage
    llm = AbacusAILLM(api_key=API_KEY)
    response = llm("Explain the concept of machine learning in simple terms.")
    print("Basic LLM Response:", response)


    # Using with LangChain chain
    chain = create_abacusai_chain(API_KEY)
    chain_response = chain.run("What is the significance of containerization in modern software development?")
    print("\nChain Response:", chain_response)"""

    
abacus_chain = create_abacusai_chain(ABACUS_API_KEY)