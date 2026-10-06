"""Chat interface for the existing permission-aware research engine."""
import streamlit as st
from core import Engine, USERS

st.set_page_config(page_title="Workplace AI", page_icon="💬", layout="centered")
st.markdown("""
<style>
.stApp {background: #f8fafc;}
[data-testid="stSidebar"] {background: #eef2f7;}
.block-container {max-width: 900px; padding-top: 2.5rem;}
h1 {letter-spacing: -1px; color: #14243b;}
[data-testid="stChatMessage"] {background: white; border: 1px solid #e5eaf1;
    border-radius: 16px; padding: 1.1rem; margin-bottom: 1rem;}
.stButton > button {border-radius: 10px;}
[data-testid="stChatInput"] {border-radius: 14px;}
</style>
""", unsafe_allow_html=True)

labels = {"employee_demo": "Employee", "manager_demo": "Manager", "hr_admin_demo": "HR Admin"}
with st.sidebar:
    st.markdown("### 💬 Workplace AI")
    st.caption("Your company knowledge assistant")
    st.divider()
    user = st.selectbox("Demo account", list(USERS), format_func=lambda value: labels[value])
    st.caption("Access role: " + labels[user])
    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []
    st.divider()
    st.markdown("Small questions. Clear answers.")
    st.caption("Find information about time off, benefits, expenses, and workplace policies.")
    with st.expander("Connection settings"):
        backend = st.radio("Answer service", ["api", "offline"],
            format_func=lambda value: "AI answers" if value == "api" else "Offline evidence preview")
        st.caption("AI answers send your question and authorized evidence to your configured API provider.")
    st.divider()
    st.caption("Portfolio demo • Fictional company data")
    st.caption("Account selection simulates identity. This demo does not provide company sign-in.")

# Never retain another role's visible answers after an account switch.
identity = (user, backend)
if st.session_state.get("chat_identity") != identity:
    st.session_state.messages = []
    st.session_state.chat_identity = identity

st.title("Workplace AI")
st.caption("Answers for your workday, based on information available to your account.")

suggestion = None
if not st.session_state.messages:
    st.markdown("### How can I help you today?")
    st.write("Ask a question about your workplace policies.")
    questions = ["How many PTO days do employees receive?",
                 "What is the remote work policy?",
                 "What benefits are available to employees?"]
    columns = st.columns(3)
    for column, question in zip(columns, questions):
        with column:
            if st.button(question, use_container_width=True):
                suggestion = question

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about policies, benefits, or time off…", max_chars=2000)
question = prompt or suggestion
if question and question.strip():
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Checking your workplace information…"):
                # Only the permission-filtered mode is exposed in this interface.
                # Visible history is not supplied to the model; questions are independent.
                result = Engine().answer(user, question, mode="D", backend=backend, k=5, candidates=5)
            answer = result["answer"]
            st.markdown(answer)
        except Exception:
            answer = "I could not connect to the answer service. Please check your local API settings and try again."
            st.error(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

st.caption("AI answers can make mistakes. Check important details against your company policies.")
