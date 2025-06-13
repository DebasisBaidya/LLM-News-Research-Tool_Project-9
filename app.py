# ✅ Phase 3 + 7 Combined: Streamlit Interface + Enhancements

import streamlit as st
import pandas as pd
from langchain_config import get_summary
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

# ⚙️ Setting up the app layout and title
st.set_page_config(page_title="LLM: News Research Tool", layout="centered")
st.markdown("""
    <div style='display: flex; flex-direction: column; align-items: center; margin-top: 2rem;'>
        <h1 style='text-align: center;'>🧠 LLM: News Research Tool</h1>
        <p style='text-align: center;'>Summarizing real-time news articles smartly using AI 🔐 Login Required</p>
    </div>
""", unsafe_allow_html=True)

# 📌 Task 7.1: Add User Authentication
# 🔐 Creating a simple login form to restrict access
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

# ♻️ Creating a reset function to clear session except login info
def reset_all():
    preserved_keys = {'authenticated'}
    for key in list(st.session_state.keys()):
        if key not in preserved_keys:
            del st.session_state[key]
    st.session_state.query_input = ""
    st.rerun()

# 📄 Creating a Unicode-safe PDF using ReportLab
def create_pdf(text_data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    textobject = c.beginText()
    textobject.setTextOrigin(inch * 1, height - inch * 1)
    textobject.setFont("Helvetica", 12)

    for line in text_data.split("\n"):
        textobject.textLine(line.strip())

    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# 📌 Task 7.2 + 3.2: Input → Summary → Output → Export
# 🧠 Handling the flow from query input to AI-generated summary and export
def generate_summary_and_output():
    st.markdown("<div style='text-align:center'><h4>📌 Try queries like:</h4></div>", unsafe_allow_html=True)
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
            response, articles = get_summary(query)
            bullet_lines = [f"• {line.strip()}" for line in response.split("•") if line.strip()]

            header_line = bullet_lines[0] if bullet_lines else ""
            formatted_summary = "\n".join(bullet_lines[1:]) if len(bullet_lines) > 1 else ""

            st.markdown(f"""
                <div style='background-color:#f0f2f6; border-left: 6px solid #4c8bf5; padding: 1rem; margin-top: 1rem;'>
                    <h4 style='margin:0;'>{header_line}</h4>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<h3 style='text-align:center;'>🧠 AI-Generated News Summary</h3>", unsafe_allow_html=True)
            st.markdown(f"<pre style='background-color:#e8f0fe; padding:1rem;'>{formatted_summary}</pre>", unsafe_allow_html=True)

            articles_text = ""
            if articles:
                st.markdown("<h3 style='text-align:center;'>📰 Articles Used for Summary</h3>", unsafe_allow_html=True)
                top_articles = articles[:3]
                for article in top_articles:
                    title = article.get("title", "No title")
                    source = article.get("source", {}).get("name", "Unknown Source")
                    date = article.get("publishedAt", "").split("T")[0]
                    url = article.get("url", "#")
                    article_block = f"- {title}\n  📅 {date} | 🏷️ {source}\n  🔗 [Read More]({url})"
                    st.markdown(article_block)
                    articles_text += f"{article_block}\n"
                st.success(f"✅ Summary extracted from {len(top_articles)} article(s).")
            else:
                st.warning("⚠️ No articles available.")

            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((query, formatted_summary))

            combined_output = f"{header_line}\n\n🧠 AI-Generated News Summary:\n{formatted_summary.strip()}\n\n📰 Articles Used for Summary:\n{articles_text.strip()}"

            colA, colB = st.columns(2)
            with colA:
                st.download_button("📥 Download as TXT", data=combined_output, file_name="summary.txt", mime="text/plain", use_container_width=True)

            pdf_output = create_pdf(combined_output)
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

# 🚀 Running the full app
handle_authentication()
generate_summary_and_output()
show_history()
