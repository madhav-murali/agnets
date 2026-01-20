from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

def writer_node(state):
    """
    Writer agent that drafts the content.
    """
    topic = state.get("topic")
    research_data = state.get("research_data")
    rag_context = state.get("rag_context", "")
    critique = state.get("critique")
    current_draft = state.get("draft")
    revision_count = state.get("revision_count", 0)

    print(f"--- Writer working on: {topic} (Revision: {revision_count}) ---")
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    if critique and current_draft:
        # Revision mode
        prompt = f"""
        You are a Senior Writer. You have a draft of an article and some feedback from an editor.
        Please rewrite the article to address the feedback.
        
        Topic: {topic}
        
        Current Draft:
        {current_draft}
        
        Editor's Feedback:
        {critique}
        
        Research Data (for reference):
        {research_data}
        
        Additional Context (RAG):
        {rag_context}
        
        Output only the revised article.
        """
        revision_count += 1
    else:
        # First draft mode
        prompt = f"""
        You are a Senior Writer. Write a comprehensive, engaging article about '{topic}'.
        Use the provided research data and context to ground your writing.
        
        Research Data:
        {research_data}
        
        Additional Context (RAG):
        {rag_context}
        
        Output only the article.
        """
        revision_count = 1

    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"draft": response.content, "revision_count": revision_count}
