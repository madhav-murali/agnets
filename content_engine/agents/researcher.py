from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from tools.search import get_search_tool

def researcher_node(state):
    """
    Research agent that looks up information about the topic.
    """
    topic = state.get("topic")
    print(f"--- Researcher working on: {topic} ---")
    
    # Initialize LLM and Tool
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    search_tool = get_search_tool()
    
    # 1. Search for data
    # We can invoke the tool directly or let the agent decide. 
    # For a deterministic flow, let's just force a search.
    search_results = search_tool.invoke(topic)
    
    # 2. Summarize findings
    prompt = f"""
    You are a Lead Researcher. 
    Summarize the following search results for a writer who will write an article about '{topic}'.
    Focus on facts, dates, key figures, and diverse perspectives.
    
    Search Results:
    {search_results}
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"research_data": response.content}
