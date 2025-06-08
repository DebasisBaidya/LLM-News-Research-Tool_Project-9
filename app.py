# ✅ Phase 3 + 7 Combined: Streamlit Interface + Enhancements

import streamlit as st
import pandas as pd
from langchain_config import llm_chain, get_summary
from fpdf import FPDF  # I’m using FPDF for PDF generation
import io

# 🧱 Setting up the app layout
st.set_page_config(page_title="LLM: News Research Tool", layout="centered")
st.markdown("""
    <div style='display: flex; flex-direction: column; align-items: center; margin-top: 2rem;'>
        <h1 style='text-align: center; margin-bottom: 0.25rem;'>🧠 LLM: News Research Tool</h1>
        <p style='text-align: center; margin-top: -0.25rem;'>Summarize real-time news articles smartly using AI 🔐 Login Required</p>
    </div>
""", unsafe_allow_html=True)

# 📌 Task 7.1: Add User Authentication
def handle_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("""
            <style>
            .login-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 75vh;
                flex-direction: column;
                gap: 0.5rem;
            }
            </style>
            <div class='login-container'>
                <h3 style='margin-bottom: 0;'>🔐 Login Required</h3>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Try: Debasis", key="username")
        password = st.text_input("Password", type="password", placeholder="Try: Baidya123", key="password")

        login_btn = st.button("Login", use_container_width=True)
        if login_btn:
            if username == "Debasis" and password == "Baidya123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect credentials. Hint: Debasis / Baidya123")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

# 📌 Function to reset session states
def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("/app.py")

# 📌 Task 7.2 + 3.2: Input → Summary → Output → Export
def generate_summary_and_output():
    st.markdown("<div style='text-align:center'><h4>📌 Try queries like:</h4></div>", unsafe_allow_html=True)

    # 📌 Example buttons in boxes and same size
    examples = ["India Election 2024", "AI in Healthcare", "Stock Market Crash", "Climate Change Effects"]
    cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with cols[i]:
            if st.button(example, use_container_width=True):
                st.session_state.query_input = example

    query = st.text_input('🔍 Enter your Query', key='query_input', placeholder="e.g., Global Warming Impact", help="Try real-time topics like AI, politics, climate, finance")
    response = ""

    st.markdown("""
        <div style='display: flex; justify-content: center; flex-direction: column; align-items: center; gap: 0.75rem; margin-top: 1rem;'>
    """, unsafe_allow_html=True)

    generate = st.button('⚡ Generate Summary', key='generate_btn', use_container_width=False)
    reset = st.button("🔄 Reset All", key='reset_btn', use_container_width=False)

    st.markdown("</div>", unsafe_allow_html=True)

    if reset:
        reset_all()

    if generate:
        if query:
            summaries = get_summary(query)
            response = llm_chain.run({"query": query, "summaries": summaries})

            st.markdown("<div style='text-align:center'><h3>🧠 AI-Generated News Summary</h3></div>", unsafe_allow_html=True)
            st.success(response[:1200] + ('...' if len(response) > 1200 else ''))

            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((query, response))

            st.download_button(
                label="📥 Download as TXT",
                data=response,
                file_name="summary.txt",
                mime="text/plain"
            )

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in response.split("\n"):
                pdf.multi_cell(0, 10, line)
            pdf_output = io.BytesIO()
            try:
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
            except UnicodeEncodeError:
                pdf_bytes = pdf.output(dest='S').encode('utf-8', errors='ignore')
            pdf_output.write(pdf_bytes)
            pdf_output.seek(0)

            st.download_button(
                label="📄 Download as PDF",
                data=pdf_output,
                file_name="summary.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Please enter a query to get the summary.")
    return query, response

# 📌 Task 7.3: View Query History
def show_history():
    if 'history' in st.session_state and st.session_state.history:
        st.markdown("---")
        st.markdown("<div style='text-align:center'><h4>📚 Past Queries</h4></div>", unsafe_allow_html=True)
        for idx, (q, r) in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.markdown(f"**{idx}. {q}**")
            st.markdown(f"> {r[:200]}...")

# ✅ Running the modular workflow
handle_authentication()
query, response = generate_summary_and_output()
show_history()
