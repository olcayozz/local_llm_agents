from typing import Dict, Any
from langgraph.graph import StateGraph, END
from graph.chains.abacus_ai_wrapper import AbacusAIWrapper
from graph.state import GraphState
from graph.node_constants import GENERATE, WEBSEARCH, RETRIEVE, ASK
import os

ABACUS_API_KEY=os.environ.get("ABACUS_API_KEY")
if not ABACUS_API_KEY:
    raise ValueError("ABACUS_API_KEY environment variable is not set.")

ABACUS_MODEL_ID=os.environ.get("ABACUS_MODEL_ID")

def create_llm_node():
    abacus_client = AbacusAIWrapper(ABACUS_API_KEY)

    def llm_node(state: Dict[str, Any]) -> Dict[str, Any]:
        # Extract prompt from state
        prompt = state.get("question", "")
        print(f"Prompt: {prompt}")
        # Call Abacus.AI API
        response = abacus_client.call_model(prompt, ABACUS_MODEL_ID)
        print(f"Prompt: {response}")
        # Update state with response
        state["response"] = response
        return state

    return llm_node

def create_embedding_node():
    abacus_client = AbacusAIWrapper(ABACUS_API_KEY)

    def embedding_node(state: Dict[str, Any]) -> Dict[str, Any]:
        # Extract text from state
        text = state.get("text", "")

        # Get embeddings from Abacus.AI
        embeddings = abacus_client.get_embeddings(text)

        # Update state with embeddings
        state["embeddings"] = embeddings
        return state

    return embedding_node

if __name__ == "__main__":
    # Example usage
    graph = StateGraph(GraphState)
    graph.add_node("LLM", create_llm_node())
    graph.add_node("Embedding", create_embedding_node())
    graph.add_edge("LLM", "Embedding")
    graph.set_entry_point("LLM")
    app = graph.compile()
    # app.get_graph().draw_mermaid_png(output_file_path="graph.png")
    
    app.invoke({"question": "What is the capital of France?"})