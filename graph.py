from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from agents.researcher import researcher_node
from agents.writer import writer_node
from agents.editor import editor_node

class AgentState(TypedDict):
    topic: str
    research_data: Optional[str]
    rag_context: Optional[str]
    draft: Optional[str]
    critique: Optional[str]
    revision_count: int
    final_content: Optional[str]

def should_continue(state):
    """
    Determines whether to go back to the writer or end.
    """
    critique = state.get("critique")
    if critique is None:
        return "end"
    else:
        return "writer"

def create_graph():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("editor", editor_node)

    # Define flow
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "editor")

    # Conditional edge
    workflow.add_conditional_edges(
        "editor",
        should_continue,
        {
            "writer": "writer",
            "end": END
        }
    )

    return workflow.compile()
