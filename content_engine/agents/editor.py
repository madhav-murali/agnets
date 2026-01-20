from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

def editor_node(state):
    """
    Editor agent that reviews the draft.
    """
    topic = state.get("topic")
    draft = state.get("draft")
    revision_count = state.get("revision_count", 0)
    
    print(f"--- Editor reviewing draft (Revision: {revision_count}) ---")
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # If we have reached max revisions, just approve to avoid infinite loops
    MAX_REVISIONS = 2
    if revision_count >= MAX_REVISIONS:
        print("Max revisions reached. Auto-approving.")
        return {"critique": None, "final_content": draft}

    prompt = f"""
    You are a Strict Editor. Review the following draft about '{topic}'.
    Check for:
    1. Clarity and flow.
    2. Alignment with the topic.
    3. Proper tone (professional yet engaging).
    
    Draft:
    {draft}
    
    If the draft is excellent and needs no changes, reply with exactly "APPROVE".
    Otherwise, provide a numbered list of specific improvements needed.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content.strip()
    
    if content == "APPROVE":
        return {"critique": None, "final_content": draft}
    else:
        return {"critique": content}
