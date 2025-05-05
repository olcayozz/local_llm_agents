from typing import Any, Dict

from langchain.schema import Document
from langchain_community.tools import DuckDuckGoSearchResults
from graph.state import GraphState


web_search_tool = DuckDuckGoSearchResults(k=1, output_format="list")

def web_search(state: GraphState) -> Dict[str, Any]:
    print("---WEB SEARCH---")
    question = state["question"]
    documents = state["documents"]

    docs = web_search_tool.invoke({"query": question})
    web_results = "".join(d["title"] for d in docs)
    web_results = Document(page_content=web_results)
    
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}