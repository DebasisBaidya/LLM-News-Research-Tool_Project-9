# ✅ Phase 3 + 7 Combined: Streamlit Interface + Enhancements

import streamlit as st
import pandas as pd
from langchain_config import get_summary
from fpdf import FPDF  # 🧾 I’m using FPDF for PDF generation
import io

# ⚙️ I’m setting up the app layout and title
st.set_page_config(page_title="LLM: News Research Tool", layout="centered")

# 📌 Task 7.1: Add User Authentication
# 🔐 I’m creating a simple login form to restrict access
def handle_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("### 🔐 Login Required")
        st.info("Use **Debasis** / **Baidya123** to log in.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if username == "Debasis" and password == "Baidya123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect credentials.")
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
    st.markdown("### 🧠 LLM: News Research Tool")
    st.markdown("Get concise summaries of current events using AI.")

    st.markdown("##### 📌 Try queries like:")
    examples = ["Air India Crash", "Ind-Pak War", "Indian Economy", "AI in Healthcare", "POK Issues"]
    example_cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(example, use_container_width=True):
                st.session_state.query_input = example

    query = st.text_area("🔍 Enter your Query", key="query_input", height=100)

    col1, col2 = st.columns(2)
    with col1:
        gen_btn = st.button("⚡ Generate Summary", use_container_width=True)
    with col2:
        reset_btn = st.button("🔄 Reset All", use_container_width=True)

    if reset_btn:
        reset_all()

    if gen_btn:
        if query:
            # 🔗 I’m calling my summarization logic from langchain_config
            response, articles = get_summary(query)

            # ✅ Format AI summary with paragraph breaks (no space lines)
            formatted_response = ""
            for point in response.split("•"):
                if point.strip():
                    formatted_response += f"• {point.strip()}\n"

            formatted_response = formatted_response.strip().replace("\n", "\n\n")

            # ✅ Summary Section
            st.markdown("### 🧠 AI-Generated News Summary:")
            st.success(formatted_response)

            # ✅ Articles Section (Top 3)
            articles_text = ""
            if articles:
                st.markdown("### 📰 Articles Used for Summary:")
                for i, article in enumerate(articles[:3], 1):
                    title = article.get("title", "No title")
                    source = article.get("source", {}).get("name", "Unknown Source")
                    date = article.get("publishedAt", "").split("T")[0]
                    url = article.get("url", "#")
                    article_block = f"- {title}\n📅 {date} | 🏷️ {source}\n🔗 [Read More]({url})"
                    st.markdown(article_block)
                    articles_text += f"{article_block}\n"
                st.success(f"✅ Summary extracted from {min(len(articles), 3)} article(s).")
            else:
                st.warning("⚠️ No articles available.")

            # 💾 I’m saving the result in history for reference
            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((query, formatted_response))

            # 💡 Show Download options (TXT + PDF)
            combined_output = f"🧠 AI-Generated News Summary:\n{formatted_response}\n\n📰 Articles Used for Summary:\n{articles_text}"

            colA, colB = st.columns(2)
            with colA:
                st.download_button("📥 Download as TXT", data=combined_output, file_name="summary.txt", mime="text/plain", use_container_width=True)

            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("ArialUnicode", "", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
            pdf.set_font("ArialUnicode", size=12)
            for line in combined_output.split("\n"):
                pdf.multi_cell(0, 10, line.strip())
            pdf_output = io.BytesIO()
            pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="ignore")
            pdf_output.write(pdf_bytes)
            pdf_output.seek(0)

            with colB:
                st.download_button("📄 Download as PDF", data=pdf_output, file_name="summary.pdf", mime="application/pdf", use_container_width=True)
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
