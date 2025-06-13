# ✅ Phase 3 + 7 Combined: Streamlit Interface + Enhancements

import streamlit as st
import pandas as pd
from langchain_config import get_summary
from fpdf import FPDF  # 🧾 I’m using FPDF for PDF generation
import io

# ⚙️ I’m setting up the app layout and title
st.set_page_config(page_title="LLM: News Research Tool", layout="centered")
st.markdown("""
    <div style='display: flex; flex-direction: column; align-items: center; margin-top: 2rem;'>
        <h1 style='text-align: center;'>🧠 LLM: News Research Tool</h1>
        <p style='text-align: center;'>Summarizing real-time news articles smartly using AI 🔐 Login Required</p>
    </div>
""", unsafe_allow_html=True)

# 📌 Task 7.1: Add User Authentication
# 🔐 I’m creating a simple login form to restrict access
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
                flex-direction: column;
                margin: 0 auto;
                padding: 1rem 2rem;
                max-width: 400px;
                background-color: #f9f9f9;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            </style>
            <div class='login-container'>
                <h3 style='margin-bottom: 1rem;'>🔐 Login Required</h3>
                <p style='font-size: 14px; color: gray;'>Hint: Username - Debasis | Password - Baidya123</p>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Try: Debasis", key="username")
        password = st.text_input("Password", type="password", placeholder="Try: Baidya123", key="password")

        if st.button("Login", use_container_width=True):
            if username == "Debasis" and password == "Baidya123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect credentials. Hint: Debasis / Baidya123")

        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

# ♻️ I’m creating a reset function that clears session except login info
def reset_all():
    preserved_keys = {'authenticated'}
    for key in list(st.session_state.keys()):
        if key not in preserved_keys:
            del st.session_state[key]
    st.session_state.query_input = ""
    st.rerun()

# 📌 Task 7.2 + 3.2: Input → Summary → Output → Export
# 🧠 I’m handling the flow from query input to AI-generated summary and export
def generate_summary_and_output():
    st.markdown("<div style='text-align:center'><h4>📌 Try queries like:</h4></div>", unsafe_allow_html=True)
    examples = ["Air India Crash", "Ind-Pak War", "Indian Economy", "AI in Healthcare", "POK Issues"]
    example_cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(example, use_container_width=True):
                st.session_state.query_input = example

    query = st.text_area("🔍 Enter your Query", key="query_input", height=100)

    # 💡 Buttons below the query field
    st.markdown("<div style='display: flex; justify-content: center; gap: 1rem;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        gen_btn = st.button("⚡ Generate Summary", use_container_width=True)
    with col2:
        reset_btn = st.button("🔄 Reset All", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if reset_btn:
        reset_all()

    if gen_btn:
        if query:
            # 🔗 I’m calling my summarization logic from langchain_config
            response, articles = get_summary(query)

            # ✅ Summary Section
            st.markdown("<div style='text-align:center'><h4>🧠 AI-Generated News Summary:</h4></div>", unsafe_allow_html=True)

            # 🧾 Format response: bold bullet ➤ subpoint
            formatted_response = ""
            for line in response.split("•"):
                if line.strip():
                    parts = line.strip().split(" - ", 1)
                    if len(parts) == 2:
                        formatted_response += f"**➤ {parts[0].strip()}**\n- {parts[1].strip()}\n\n"
                    else:
                        formatted_response += f"- {parts[0].strip()}\n\n"
            st.success(formatted_response.strip())

            # ✅ Articles Section
            articles_text = ""
            if articles:
                st.markdown("<div style='text-align:center'><h4>📰 Articles Used for Summary:</h4></div>", unsafe_allow_html=True)
                for i, article in enumerate(articles, 1):
                    title = article.get("title", "No title")
                    source = article.get("source", {}).get("name", "Unknown Source")
                    date = article.get("publishedAt", "").split("T")[0]
                    url = article.get("url", "#")
                    article_block = f"- {i}. **{title}**  \n📅 {date} | 🏷️ {source}  \n🔗 [Read More]({url})"
                    st.markdown(article_block)
                    articles_text += f"{title}\n📅 {date} | 🏷️ {source}\n🔗 {url}\n\n"

                st.success(f"✅ Summary extracted from {len(articles)} article(s).")
            else:
                st.warning("⚠️ No articles available.")

            # 💾 I’m saving the result in history for reference
            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((query, formatted_response))

            # 💡 Show Download options (TXT + PDF)
            combined_output = f"🧠 AI-Generated News Summary:\n\n{formatted_response.strip()}\n\n📰 Articles Used for Summary:\n\n{articles_text.strip()}"

            st.markdown("<div style='display: flex; justify-content: center; gap: 1rem;'>", unsafe_allow_html=True)
            colA, colB = st.columns(2)

            with colA:
                st.download_button("📥 Download as TXT", data=combined_output, file_name="summary.txt", mime="text/plain", use_container_width=True)

            # 🧾 PDF Export with encoding fix
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in combined_output.split("\n"):
                try:
                    pdf.multi_cell(0, 10, line.encode("latin-1", "replace").decode("latin-1"))
                except:
                    pdf.multi_cell(0, 10, "[Encoding Error]")
            pdf_output = io.BytesIO()
            pdf_bytes = pdf.output(dest="S").encode("latin-1")
            pdf_output.write(pdf_bytes)
            pdf_output.seek(0)
            with colB:
                st.download_button("📄 Download as PDF", data=pdf_output, file_name="summary.pdf", mime="application/pdf", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a query first.")

# 📌 Task 7.3: View past searches
def show_history():
    if 'history' in st.session_state and st.session_state.history:
        st.markdown("---")
        st.subheader("📚 Past Queries")
        for idx, (q, r) in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.markdown(f"**{idx}. {q}**")
            st.markdown(f"> {r[:200]}...")

# 🚀 I’m executing everything now
handle_authentication()
generate_summary_and_output()
show_history()
