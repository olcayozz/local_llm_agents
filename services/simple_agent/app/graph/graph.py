import sys
import os
#from pyppeteer import MermaidDrawMethod

# Update the sys.path to include the parent directory of the 'app' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from graph.node_constants import GENERATE, WEBSEARCH, RETRIEVE, BYE
from graph.nodes.generate import generate
from graph.nodes.web_search import web_search
from graph.nodes.retrieve import retrieve
from graph.state import GraphState
from graph.chains.llm_router import question_router, RouteQuery


load_dotenv()

def check_bye(state: GraphState) -> bool:  
    print("---CHECK BYE---")
    question = state["question"]
    if question.lower() == "bye":
        state["bye"] = True
        return True
    return False    

def route_question(state: GraphState) -> str:
    print("---ROUTE QUESTION---")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})
    if source.datasource == WEBSEARCH:
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE

workflow = StateGraph(GraphState)
workflow.set_conditional_entry_point(
    route_question,
    {
        WEBSEARCH: WEBSEARCH,
        RETRIEVE: RETRIEVE,
        BYE: END,
    },
)
workflow.add_node(RETRIEVE, retrieve) 
workflow.add_node(GENERATE, generate) 
workflow.add_node(WEBSEARCH, web_search)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(RETRIEVE, GENERATE)
workflow.add_edge(GENERATE, END)
workflow.add_edge(WEBSEARCH, END)


"""workflow.add_conditional_edges(
    GENERATE,
    check_bye,
    {
        BYE: END,
        False: RETRIEVE,
    },
)"""
app = workflow.compile()
app.get_graph().draw_ascii()
#.draw_mermaid_png(output_file_path="graph.png", max_retries=5, retry_delay=2.0)
