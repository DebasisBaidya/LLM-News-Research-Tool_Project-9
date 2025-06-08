# ✅ Phase 3 + 7 Combined: Streamlit Interface + Enhancements (Improved UI, Centered Buttons)

import streamlit as st
import pandas as pd
from fpdf import FPDF  # I’m using FPDF for PDF generation
from langchain_config import llm_chain, get_summary

# 🧱 Setting up the app layout
st.set_page_config(page_title="LLM: News Research Tool", layout="centered")

# I’m setting a title for the header
st.markdown("""
    <div style='text-align: center;'>
        <h1>🧠 LLM: News Research Tool</h1>
        <h5>Summarize latest news articles using Groq LLM + NewsAPI</h5>
    </div>
""", unsafe_allow_html=True)

# 📌 Task 7.1: Add User Authentication (Now with ID + Password)
def handle_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False  # I’m initializing login status

    if not st.session_state.authenticated:
        st.markdown("""
            <div style='text-align: center;'>
                <h3>🔐 Login Required</h3>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=True):
            user_id = st.text_input("User ID", placeholder="Enter ID")
            password = st.text_input("Password", type="password", placeholder="Enter Password")
            st.caption("💡 Demo Login → ID: Debasis | Password: Baidya123")  # I’m showing help text
            login_btn = st.form_submit_button("🔓 Login")
            if login_btn:
                if user_id == "Debasis" and password == "Baidya123":
                    st.session_state.authenticated = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid ID or Password.")
        st.stop()

# 📌 Task 7.2 + 3.2: Input → Summary → Output → Export
def generate_summary_and_output():
    with st.expander("🔍 Click to See Example News Topics"):
        st.markdown("""
            - AI in Finance
            - Lok Sabha Elections
            - Apple Vision Pro Launch
            - Climate Change
            - Stock Market Today
        """)

    query = st.text_area('✍️ Enter your News Topic', height=100, key="query_input")

    # I’m centrally aligning action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    response = ""
    with col2:
        if st.button("📄 Get News Summary"):
            if query:
                summaries = get_summary(query)  # I’m fetching news
                brief = summaries[:1200]  # I’m limiting input for concise output
                response = llm_chain.run({"query": query, "summaries": brief})  # I’m generating summary
                st.markdown("### 🧠 AI-Generated Summary")
                st.success(response)

                if 'history' not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.append((query, response))

                st.download_button("📥 Download Summary (TXT)", response, file_name="summary.txt")

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in response.split("\n"):
                    pdf.multi_cell(0, 10, line)
                pdf_output = "/tmp/summary.pdf"
                pdf.output(pdf_output)
                with open(pdf_output, "rb") as f:
                    st.download_button("📄 Download Summary (PDF)", data=f, file_name="summary.pdf", mime="application/pdf")
            else:
                st.warning("Please enter a query to get the summary.")

    with col2:
        if st.button("🔁 Reset All"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]  # I’m clearing session state
            st.experimental_rerun()

    return query, response

# 📌 Task 7.3: View Query History
def show_history():
    if 'history' in st.session_state and st.session_state.history:
        st.markdown("---")
        st.markdown("### 📚 Past Queries")
        for idx, (q, r) in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.markdown(f"**{idx}. {q}**")
            st.markdown(f"> {r[:200]}...")

# ✅ Running the modular workflow
handle_authentication()
query, response = generate_summary_and_output()
show_history()
