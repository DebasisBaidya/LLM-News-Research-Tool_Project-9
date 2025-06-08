# ✅ Phase 3 + 7 Combined: Streamlit Interface + Enhancements

import streamlit as st
import pandas as pd
from langchain_config import llm_chain, get_summary
from fpdf import FPDF  # I’m using FPDF for PDF generation
import io

# 🧱 Setting up the app layout
st.set_page_config(page_title="LLM: News Research Tool", layout="centered")
st.markdown("""
    <h1 style='text-align: center;'>🧠 LLM: News Research Tool</h1>
    <p style='text-align: center;'>Enter your query to summarize live news from the web</p>
""", unsafe_allow_html=True)

# 📌 Task 7.1: Add User Authentication
def handle_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False  # I’m initializing login status

    if not st.session_state.authenticated:
        with st.form(key="login_form", clear_on_submit=True):
            st.markdown("""<div style='text-align:center'><h3>🔐 Login Required</h3></div>""", unsafe_allow_html=True)
            st.text_input("Username", placeholder="Try: Debasis", key="username")  # I’m collecting username
            st.text_input("Password", type="password", placeholder="Try: Baidya123", key="password")  # I’m collecting password
            submitted = st.form_submit_button("Login")

            if submitted:
                if st.session_state.username == "Debasis" and st.session_state.password == "Baidya123":
                    st.session_state.authenticated = True  # I’m setting authentication flag
                    st.success("Login successful!")
                else:
                    st.error("Incorrect credentials. Hint: Debasis / Baidya123")
        st.stop()  # I’m stopping execution until login passes

# 📌 Function to reset session states
def reset_all():
    for key in ["query_input", "history"]:
        if key in st.session_state:
            del st.session_state[key]  # I’m resetting query input and history
    st.experimental_set_query_params()  # I’m clearing URL query state
    st.success("Reset done! You may enter a new query now.")

# 📌 Task 7.2 + 3.2: Input → Summary → Output → Export
def generate_summary_and_output():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center'><h4>📌 Try queries like: 'India Election 2024', 'AI in Healthcare', 'Stock Market Crash'</h4></div>", unsafe_allow_html=True)

    query = st.text_input('🔍 Enter your Query', key='query_input', placeholder="e.g., Global Warming Impact", label_visibility="visible")  # I’m asking for user query
    response = ""

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        generate = st.button('⚡ Generate Summary')  # I’m triggering news search and summary
    with col2:
        reset = st.button("🔄 Reset All")  # I’m resetting query and output

    if reset:
        reset_all()

    if generate:
        if query:
            summaries = get_summary(query)  # I’m fetching news article summaries
            response = llm_chain.run({"query": query, "summaries": summaries})  # I’m generating the concise summary
            response = response[:1000] + ("..." if len(response) > 1000 else "")  # I’m trimming the summary to keep it readable
            st.markdown("<div style='text-align:center'><h3>🧠 AI-Generated News Summary</h3></div>", unsafe_allow_html=True)
            st.success(response)

            if 'history' not in st.session_state:
                st.session_state.history = []  # I’m initializing query history
            st.session_state.history.append((query, response))  # I’m storing history

            # 📝 Adding download buttons
            st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download as TXT",
                data=response,
                file_name="summary.txt",
                mime="text/plain"
            )

            # Creating PDF in-memory
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in response.split("\n"):
                pdf.multi_cell(0, 10, line)
            pdf_output = io.BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)

            st.download_button(
                label="📄 Download as PDF",
                data=pdf_output,
                file_name="summary.pdf",
                mime="application/pdf"
            )
            st.markdown("</div>", unsafe_allow_html=True)
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
