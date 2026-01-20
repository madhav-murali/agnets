import streamlit as st
import os
from dotenv import load_dotenv
from graph import create_graph
# RAG is optional, removing strict dependency if not used, but keeping import
try:
    from tools.rag import SimpleRAG
except ImportError:
    SimpleRAG = None

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Collab Content Engine", layout="wide")

st.title("🤖 Collaborative Content Synthesis Engine")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    st.info("Ensure OPENAI_API_KEY and TAVILY_API_KEY are set in .env")
    
    # RAG Upload
    st.subheader("Knowledge Base (RAG)")
    uploaded_files = st.file_uploader("Upload reference documents", accept_multiple_files=True, type=['txt', 'md'])
    
    rag_context = ""
    if uploaded_files:
        rag_context = ""
        for uploaded_file in uploaded_files:
             uploaded_file.seek(0)
             rag_context += uploaded_file.read().decode("utf-8") + "\n\n"
        
        st.success(f"Loaded {len(uploaded_files)} documents.")
        if len(rag_context) > 10000:
            rag_context = rag_context[:10000] + "...(truncated)"
    else:
        st.write("No documents uploaded. Agents will use Search + Training data.")

# Main Area
topic = st.text_input("Enter a topic for the content:", placeholder="e.g., The Future of Quantum Computing in Finance")

if st.button("Generate Content"):
    if not topic:
        st.error("Please enter a topic.")
    else:
        st.write(f"🚀 Starting synthesis for: **{topic}**")
        
        # Initialize Graph
        workflow = create_graph()
        
        # Initial State
        initial_state = {
            "topic": topic,
            "revision_count": 0,
            "rag_context": rag_context
        }
        
        final_output_content = None
        
        # Run graph
        with st.status("Agents are working...", expanded=True) as status:
            st.write("🔍 **Researcher** is gathering information...")
            
            for event in workflow.stream(initial_state):
                for key, value in event.items():
                    if key == "researcher":
                        st.write("✅ **Researcher** finished.")
                        with st.expander("See Research Data"):
                            st.write(value.get("research_data", "No data"))
                    
                    elif key == "writer":
                        rev = value.get("revision_count", 0)
                        st.write(f"✍️ **Writer** finished draft (Iter {rev}).")
                        with st.expander(f"See Draft {rev}"):
                            st.write(value.get("draft", ""))
                    
                    elif key == "editor":
                        critque = value.get("critique")
                        if critque:
                            st.write(f"🧐 **Editor** requested changes.")
                            with st.expander("See Critique"):
                                st.write(critque)
                        else:
                            st.write("✅ **Editor** approved!")
                            final_output_content = value.get("final_content")

            status.update(label="Workflow Complete!", state="complete", expanded=False)

        if final_output_content:
            st.header("Final Article")
            st.markdown(final_output_content)
            st.balloons()
        else:
            st.warning("Workflow finished but no final content was returned (possibly hit max revisions). Check drafts above.")
