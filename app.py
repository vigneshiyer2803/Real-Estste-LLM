import os
import streamlit as st
from openai import OpenAI

# ========== SETUP ==========

# Load API key securely from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Initialize Groq-compatible OpenAI client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["OPENAI_API_KEY"]
)

# ========== REAL ESTATE CHAT FUNCTION ==========

def ask_realestate_assistant(messages):
    """Send chat messages to the Groq Llama model and return the assistant’s response."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ========== STREAMLIT UI ==========

st.set_page_config(page_title="🏠 Real Estate Assistant", layout="centered")
st.title("🏠 Real Estate Assistant")
st.markdown("Your AI-powered guide for **Real Estate** insights, property advice, and investment decisions.")

# ========== SESSION STATE INIT ==========

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an expert Real Estate Assistant. Provide helpful, factual, and clear responses about real estate, property investment, pricing, and market trends."}
    ]

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

# ========== FIRST PROMPT ==========

if not st.session_state.start_chat:
    with st.form("initial_form"):
        user_input = st.text_area("💬 Ask your first question about real estate:", height=100, placeholder="e.g., What are the best cities to invest in property in 2025?")
        submitted = st.form_submit_button("Send")

        if submitted and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Analyzing market trends..."):
                answer = ask_realestate_assistant(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.session_state.start_chat = True
            st.rerun()

# ========== FOLLOW-UP CHAT ==========

else:
    st.markdown("### 🗨️ Conversation History")

    for msg in st.session_state.chat_history[1:]:  # Skip system prompt
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**🤖 Assistant:** {msg['content']}")

    with st.form("followup_form"):
        followup_input = st.text_area("💬 Ask another question:", height=100, placeholder="e.g., How can I evaluate a property's ROI?")
        followup_submitted = st.form_submit_button("Send")

        if followup_submitted and followup_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": followup_input})
            with st.spinner("Thinking..."):
                followup_answer = ask_realestate_assistant(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": followup_answer})
            st.rerun()
