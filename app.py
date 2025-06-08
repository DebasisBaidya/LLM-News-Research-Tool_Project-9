# ✅ Phase 3 + 7 Combined: Streamlit Interface + Enhancements

import streamlit as st
import pandas as pd
from langchain_config import llm_chain, get_summary
from io import BytesIO
from fpdf import FPDF  # I’m using FPDF for PDF generation

# 🧱 I’m setting up the app layout
st.set_page_config(page_title="Universal News Summarizer", layout="centered")

# 🧾 I’m customizing title and help text with login credentials
st.title('📰 Universal News Summarizer')
st.markdown('Enter your query below to get a summary of the latest relevant news articles.')
st.info("🔐 Login Credentials — **ID:** Debasis | **Password:** Baidya123")

# 📌 Task 7.1: I’m creating User Authentication with both ID & Password
def handle_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False  # I’m initializing login status

    if not st.session_state.authenticated:
        st.subheader("🔐 Login Required")
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Enter ID")
        with col2:
            password = st.text_input("Enter Password", type="password")

        if st.button("Login"):
            if username == "Debasis" and password == "Baidya123":  # I’m checking credentials
                st.session_state.authenticated = True
            else:
                st.error("❌ Incorrect ID or Password.")
        st.stop()  # I’m blocking app access until authenticated

# 📌 Task 7.2 + 3.2: I’m creating input → summary → output → download
def generate_summary_and_output():
    st.markdown("### 🔍 Enter your Query Below")

    # I’m adding example buttons that autofill query box
    with st.expander("💡 Click for Example Topics", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("India Election 2024"):
                st.session_state.query_input = "India Election 2024"
        with col2:
            if st.button("Nvidia AI Chips"):
                st.session_state.query_input = "Nvidia AI Chips"
        with col3:
            if st.button("IPL 2025"):
                st.session_state.query_input = "IPL 2025 Highlights"

    # I’m adding input box for user query
    query = st.text_input('', key='query_input', placeholder='Type your news topic here...')
    response = ""

    # I’m wrapping Get Summary and Reset buttons side by side
    col1, col2 = st.columns([1, 1])
    with col1:
        get_button = st.button('🧠 Get News Summary')
    with col2:
        reset_button = st.button('🔄 Reset All')

    if reset_button:
        st.session_state.query_input = ''
        st.session_state.pop('history', None)
        st.experimental_set_query_params()  # I’m doing a soft page reset
        st.success("Reset complete. You can start fresh!")

    if get_button:
        if query:
            summaries = get_summary(query)  # I’m fetching relevant news
            response = llm_chain.run({"query": query, "summaries": summaries})  # I’m generating LLM response
            st.markdown("### 📌 AI-Generated Summary")
            st.success(response)

            # I’m saving the query-response pair in history
            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((query, response))

            # 📝 I’m providing text download
            st.download_button(
                label="📥 Download as Text",
                data=response,
                file_name="summary.txt",
                mime="text/plain"
            )

            # 📄 I’m providing PDF download too
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in response.split('\n'):
                pdf.multi_cell(0, 10, line)
            pdf_output = BytesIO()
            pdf.output(pdf_output)
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

# 📌 Task 7.3: I’m creating a section to show last 5 queries
def show_history():
    if 'history' in st.session_state and st.session_state.history:
        st.markdown("---")
        st.markdown("### 📚 Past Queries")
        for idx, (q, r) in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.markdown(f"**{idx}. {q}**")
            st.markdown(f"> {r[:200]}...")

# ✅ Running everything in order
handle_authentication()
query, response = generate_summary_and_output()
show_history()
