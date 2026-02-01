import streamlit as st
import os
from config import Config
from rag_engine import RAGEngine
from feedback_manager import FeedbackManager

# Page Config
st.set_page_config(page_title="Agentic AI RAG", layout="wide")

# Initialize Session State
if "rag" not in st.session_state:
    st.session_state.rag = RAGEngine()
    # Check if DB is init
    if not os.path.exists(Config.CHROMA_PATH):
         # If using the CLI init, this might not be needed, but good for safety
         pass 

if "fb_manager" not in st.session_state:
    st.session_state.fb_manager = FeedbackManager()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "feedback_queue" not in st.session_state:
    st.session_state.feedback_queue = None

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("Re-Initialize Database"):
        with st.spinner("Re-indexing PDF..."):
            st.session_state.rag.initialize_database(Config.PDF_PATH, force=True)
        st.success("Database Re-created!")
    
    st.divider()
    st.subheader("📊 System Stats")
    st.caption(f"Model: {Config.MODEL_NAME}")
    
    st.divider()
    st.subheader("📝 Learning History")
    
    # --- FIX START: Use the correct method name 'get_stats' ---
    stats = st.session_state.fb_manager.get_stats()
    st.metric("Total Feedback", stats['total'])
    st.metric("Corrections Learned", stats['corrections'])
    # --- FIX END ---

# Main Chat Interface
st.title("🤖 Agentic AI Expert")
st.caption("Ask me about Agentic AI capabilities, use cases, or architecture.")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ask a question..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. RAG Retrieval & Generation
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # A. Check for Learned Feedback first (RL Loop)
            learned_correction = st.session_state.fb_manager.get_correction_for_pattern(prompt)
            
            if learned_correction:
                response_text = f"**[Learned Answer]** {learned_correction['correction']}"
                sources = []
                st.markdown(response_text)
            else:
                # B. Standard RAG
                # Note: changed query() to search() to match vector_store.py
                chunks = st.session_state.rag.vector_store.search(prompt, top_k=5)
                
                # Apply Feedback Weights (RL) - Placeholder for now
                # chunks = st.session_state.fb_manager.apply_feedback_to_retrieval(chunks, relevant_fb)
                
                # Generate
                response_text = st.session_state.rag.answer_query(prompt, chunks)
                st.markdown(response_text)

    # 3. Store History & Prepare for Feedback
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response_text
    })
    st.session_state.feedback_queue = {"query": prompt, "response": response_text}
    st.rerun()

# Feedback Section (Appears after last bot message)
if st.session_state.feedback_queue:
    st.divider()
    st.caption("Was this answer correct?")
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("👍 Correct"):
            st.session_state.fb_manager.store_feedback(
                st.session_state.feedback_queue["query"],
                st.session_state.feedback_queue["response"],
                "positive"
            )
            st.toast("Feedback recorded: Positive reinforcement!")
            st.session_state.feedback_queue = None
            st.rerun()
            
    with col2:
        with st.expander("👎 Incorrect (Provide Correction)"):
            with st.form("correction_form"):
                correction = st.text_area("What is the correct answer?")
                if st.form_submit_button("Submit Correction"):
                    st.session_state.fb_manager.store_feedback(
                        st.session_state.feedback_queue["query"],
                        st.session_state.feedback_queue["response"],
                        "negative",
                        correction=correction
                    )
                    st.toast("Feedback recorded: Correction learned!")
                    st.session_state.feedback_queue = None
                    st.rerun()