import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq

# --- 1. CONFIGURATION ---
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Admissions AI", page_icon="🎓")

# --- 2. SIDEBAR (CLEANED) ---
with st.sidebar:
    st.title("🔧 Controls")
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()



# --- 3. DATABASE & TOOL ---
def check_application_status(student_id: str) -> str:
    """Retrieves admission status for a specific student ID."""
    try:
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS students (student_id TEXT, name TEXT, status TEXT, notes TEXT)")
        # Insert dummy data if empty
        cursor.execute("INSERT OR IGNORE INTO students VALUES ('STU-1001', 'Alice', 'ACCEPTED', 'Scholarship Awarded')")
        cursor.execute("INSERT OR IGNORE INTO students VALUES ('STU-1002', 'Bob', 'REJECTED', 'Low GPA')")
        conn.commit()

        cursor.execute("SELECT name, status, notes FROM students WHERE student_id=?", (student_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return f"Student: {row[0]} | Status: {row[1]} | Notes: {row[2]}"
        else:
            return "Student ID not found."
    except Exception as e:
        return f"Database Error: {str(e)}"


# --- 4. THE AGENT (WITH GROUNDING) ---
@st.cache_resource
def get_agent():
    return Agent(
        model=Groq(id="llama-3.3-70b-versatile", api_key=api_key),
        tools=[check_application_status],
        instructions=[
            # --- IDENTITY ---
            "You are an Admissions Officer for Tech University.",

            # --- SCOPE GUARDRAILS ---
            "Your goal is to check application status using the tool.",
            "If the user asks about non-admission topics, politely refuse.",

            # --- EMOTIONAL INTELLIGENCE ---
            "ALLOW emotional reactions (e.g., 'Thank God', 'Oh no'). Respond with empathy.",

            # --- CRITICAL: CLOSING THE LOOP (THE FIX) ---
            "If the user says 'Ok', 'Thanks', 'Cool', 'Hmm ok', or 'Bye', do NOT ask for the ID again.",
            "Instead, simply reply: 'You're welcome! Have a great day.' or 'Let us know if you need anything else.'",
            "Recognize when the conversation is finished.",

            # --- ADVICE GROUNDING ---
            "If a rejected student asks for help, offer ONLY general academic advice.",
            "Do NOT mention specific 'Summer Programs' or 'Waivers' unless in the database.",

            # --- TOOL USAGE ---
            "Use the tool ONLY when a Student ID (STU-XXXX) is provided.",
            "Do NOT show the tool output or technical logs."
        ],
        show_tool_calls=False,
        markdown=True
    )


agent = get_agent()

# --- 5. THE CHAT UI ---
st.title("🎓 University Admissions AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle Input
if prompt := st.chat_input("Ask about admission status..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                # Manual context injection for memory
                context_prompt = f"History: {st.session_state.messages[-3:]}\nUser: {prompt}"
                response = agent.run(context_prompt)
                st.write(response.content)
                st.session_state.messages.append({"role": "assistant", "content": response.content})
            except Exception as e:
                st.error(f"Error: {e}")