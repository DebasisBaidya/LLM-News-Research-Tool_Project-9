import streamlit as st
import pandas as pd
from langchain_config import llm_chain, get_summary
from fpdf import FPDF  # 🧾 for generating downloadable PDF
import io

# ⚙️ Setting up the app layout and title
st.set_page_config(page_title="LLM: News Research Tool", layout="centered")
st.markdown("""
    <div style='display: flex; flex-direction: column; align-items: center; margin-top: 2rem;'>
        <h1 style='text-align: center; margin-bottom: 0.25rem;'>🧠 LLM: News Research Tool</h1>
        <p style='text-align: center; margin-top: 0.25rem;'>Summarizing real-time news articles smartly using AI 🔐 Login Required</p>
    </div>
""", unsafe_allow_html=True)

# 🔐 Handling login authentication for the app
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

        # 👤 Asking for user credentials
        username = st.text_input("Username", placeholder="Try: Debasis", key="username")
        password = st.text_input("Password", type="password", placeholder="Try: Baidya123", key="password")

        # 🔘 Handling login button click
        login_btn = st.button("Login", use_container_width=True)
        if login_btn:
            if username == "Debasis" and password == "Baidya123":
                st.session_state.authenticated = True
                st.rerun()  # 🔁 Refreshing page on success
            else:
                st.error("❌ Incorrect credentials. Hint: Debasis / Baidya123")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

# ♻️ Resetting the app while keeping login state
def reset_all():
    preserved_keys = {'authenticated'}  # 🔐 Keeping login info safe
    for key in list(st.session_state.keys()):
        if key not in preserved_keys:
            del st.session_state[key]
    st.session_state.query_input = ""  # 🧹 Clearing input
    st.rerun()  # 🔁 Reloading the app

# 🧠 Handling the main flow: input → AI summary → download
def generate_summary_and_output():
    st.markdown("<div style='text-align:center'><h4>📌 Try queries like:</h4></div>", unsafe_allow_html=True)

    # 💡 Showing example query buttons
    examples = ["Indian Economy", "AI in Healthcare", "Stock Market Crash", "POK Issues"]

    # 🎨 Styling buttons for consistency
    st.markdown("""
        <style>
            .stButton > button {
                width: 100% !important;
                border-radius: 8px;
                padding: 0.5rem 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # 🔘 Creating button grid for examples
    example_cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(example, use_container_width=True):
                st.session_state.query_input = example  # ✍️ Auto-filling clicked example

    response = ""  # 🧾 Initializing response holder

    # ✏️ Showing the main input box for user query
    query = st.text_area(
        '🔍 Enter your Query',
        key='query_input',
        placeholder="e.g., Global Warming Impact",
        height=100,
        help="Try real-time topics like AI, politics, climate, finance"
    )

    # 🚀 Adding "Generate" and "Reset" buttons
    st.markdown("<div style='display:flex; justify-content:center; gap:1rem; margin-top:1rem;'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        generate = st.button('⚡ Generate Summary', key='generate_btn', use_container_width=True)
    with col2:
        reset = st.button("🔄 Reset All", key='reset_btn', use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if reset:
        reset_all()  # 🔁 Resetting app if clicked

    if generate:
        if query:
            # 🤖 Getting AI-generated summary from Langchain
            summaries = get_summary(query)
            response = llm_chain.run({"query": query, "summaries": summaries})

            # 🧾 Showing the summary box
            st.markdown("<div style='text-align:center'><h3>🧠 AI-Generated News Summary</h3></div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style='background-color: #e8f5e9; padding: 1rem; border-radius: 10px;'>
                    {response}
                </div>
            """, unsafe_allow_html=True)

            # 🕓 Saving to history for later use
            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((query, response))

            # 📥 Download options (TXT & PDF)
            download_col = st.columns([1, 1])
            with download_col[0]:
                st.download_button(
                    label="📅 Download as TXT",
                    data=response,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            # 📄 Generating the PDF version
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

            with download_col[1]:
                st.download_button(
                    label="📄 Download as PDF",
                    data=pdf_output,
                    file_name="summary.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ Please enter a query to get the summary.")
    return query, response

# 📚 Showing the last 5 queries and summaries
def show_history():
    if 'history' in st.session_state and st.session_state.history:
        st.markdown("---")
        st.markdown("<div style='text-align:center'><h4>📚 Past Queries</h4></div>", unsafe_allow_html=True)
        for idx, (q, r) in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.markdown(f"**{idx}. {q}**")
            st.markdown(f"> {r[:200]}...")

# 🔁 Running everything in proper order
handle_authentication()
query, response = generate_summary_and_output()
show_history()
