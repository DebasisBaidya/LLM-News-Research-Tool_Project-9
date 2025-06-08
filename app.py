# ✅ Phase 3 + 7 Combined: Streamlit Interface + Enhancements

import streamlit as st
import pandas as pd
from langchain_config import llm_chain, get_summary

# 🧱 Setting up the app layout
st.set_page_config(page_title="Equity Research News Tool", layout="centered")
st.title('📰 Equity Research News Tool')
st.markdown('Enter your query below to get a summary of the latest relevant news articles.')

# 📌 Task 7.1: Add User Authentication
def handle_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False  # I’m initializing login status

    if not st.session_state.authenticated:
        st.subheader("🔐 Login Required")
        password = st.text_input("Enter Password", type="password")  # I’m asking for password
        if st.button("Login"):
            if password == "nextgen2025":  # I’m checking password (can customize)
                st.session_state.authenticated = True
                st.rerun() # I’m reloading after successful login                              
            else:
                st.error("Incorrect password. Please try again.")
        st.stop()  # I’m blocking app access until authenticated

# 📌 Task 7.2 + 3.2: Input → Summary → Output → Export
def generate_summary_and_output():
    query = st.text_input('🔍 Enter your Query')  # I’m asking for user query
    response = ""

    if st.button('Get News Summary'):
        if query:
            summaries = get_summary(query)  # I’m fetching relevant news
            response = llm_chain.run({"query": query, "summaries": summaries})  # I’m generating LLM response
            st.markdown("### 🧠 AI-Generated Summary")
            st.success(response)

            if 'history' not in st.session_state:
                st.session_state.history = []  # I’m initializing query history
            st.session_state.history.append((query, response))  # I’m storing current query

            st.download_button(
                label="📥 Download Summary",
                data=response,
                file_name="summary.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please enter a query to get the summary.")
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
