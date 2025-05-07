from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
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


class AbacusAILLM(LLM):
    """Wrapper around Abacus.AI large language models using official API client."""

    def __init__(
        self,
        api_key: str,
        model_name: str = ABACUS_MODEL_ID,
        temperature: float = 0.1,
        max_tokens: int = 50,
        **kwargs: Any,
    ):
        """Initialize the Abacus.AI LLM wrapper.

        Args:
            api_key (str): Your Abacus.AI API key
            model_name (str, optional): Model to use. Defaults to "claude-3-sonnet".
            temperature (float, optional): Sampling temperature. Defaults to 0.7.
            max_tokens (int, optional): Maximum tokens in response. Defaults to 1000.
        """
        super().__init__(**kwargs)

        # Initialize the Abacus.AI API client
        self.client = ApiClient(api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "abacus_ai"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Execute the call to Abacus.AI using the API client.

        Args:
            prompt (str): The prompt to send to the API
            stop (Optional[List[str]], optional): Stop sequences. Defaults to None.
            run_manager (Optional[CallbackManagerForLLMRun], optional): Callback manager.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The model's response text

        Raises:
            Exception: If the API call fails
        """
        try:
            # Create the chat completion using the API client
            response = self.client.create_chat_completion(
                model=self.model_name,
                prompt = prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stop_sequences=stop if stop else None
            )

            # Extract the response text
            # Note: Adjust the response parsing based on actual API response structure
            return response.content

        except Exception as e:
            raise Exception(f"Error calling Abacus.AI API: {str(e)}")


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
    return LLMChain(llm=llm, prompt=prompt)


def example_usage():
    """Example usage of the AbacusAILLM wrapper."""

    # Replace with your actual API key
    API_KEY = ABACUS_API_KEY

    # Basic LLM usage
    llm = AbacusAILLM(api_key=API_KEY)
    response = llm("Explain the concept of machine learning in simple terms.")
    print("Basic LLM Response:", response)


    # Using with LangChain chain
    chain = create_abacusai_chain(API_KEY)
    chain_response = chain.run("What is the significance of containerization in modern software development?")
    print("\nChain Response:", chain_response)

if __name__ == "__main__":
    example_usage()