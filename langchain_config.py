# ✅ Phase 1: Environment Setup (Completed)
# -----------------------------------------------------
# 📌 Task 1.1: Install Required Libraries
# - I’m installing the essential Python libraries to handle LLM logic, UI, and news scraping.
# - The required libraries are: langchain, streamlit, newsapi-python, groq, and python-dotenv

# ✅ Installation Command:
# pip install langchain streamlit newsapi-python groq python-dotenv

# 📌 Task 1.2: Obtain API Keys
# - I’m generating the required API keys to access Groq’s LLM and NewsAPI.
# - Getting Groq API key from: https://console.groq.com/keys
# - Getting NewsAPI key from: https://newsapi.org/

# 📌 Task 1.3: Stored in 'Streamlit Secret TOML' file

# ✅ Phase 1 → Phase 3: Environment Setup + LangChain + Summarization Logic

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient

# ✅ Phase 1: API Integration
# 🔐 Loading API keys from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]
news_api_key = st.secrets["NEWS_API_KEY"]

# ✅ Phase 2: Model Initialization
# 🧠 Initializing Groq’s LLaMA3 model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# ✅ Phase 3.1: Enhanced Prompt Template for Detailed Summaries
enhanced_template = """
You are a highly factual AI news summarizer.

Using the provided real-time news article content and user query, generate a clear and informative summary of the current situation.

✅ The summary should:
- Be factually accurate and unbiased
- Contain 4 to 6 bullet points
- Each point must follow the format: MainPoint - Subpoint
- Avoid repetition of query
- Do not generate any intro or closing lines

Do NOT make anything up — base everything strictly on the provided content.

---

📝 User Query:
{query}

📰 News Article Content:
{summaries}

---

📌 Provide the final formatted bullet-point summary below, using • as bullet symbol:
"""

# 🎯 Prompt template with required input variables
enhanced_prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])

# 🔗 LLMChain that links the prompt and model
llm_chain = LLMChain(prompt=enhanced_prompt, llm=llm)

# ✅ Phase 3.2: News Fetching
# 📡 Initializing NewsAPI client
newsapi = NewsApiClient(api_key=news_api_key)

# 🔍 Fetching articles using the query
def get_news_articles(query):
    articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=10)
    if not articles['articles']:
        st.warning("⚠️ No current articles found for this query.")
    return articles['articles']

# 🧾 Extracting summary content
def summarize_articles(articles):
    summaries = [
        article.get('description') or article.get('content') or ''
        for article in articles if article.get('description') or article.get('content')
    ]
    return ' '.join(summaries)

# ✅ Phase 3.3: Final Summary Output
# 📋 Generating summary + article info
def get_summary(query):
    articles = get_news_articles(query)
    summaries = summarize_articles(articles)

    if not summaries.strip():
        st.error("❌ No summary content could be extracted.")
        return "⚠️ No content found to summarize. Try another topic.", []

    used_articles = [article for article in articles if article.get('description') or article.get('content')]

    # 🤖 Generate and return the bullet-point summary and article metadata
    summary_output = llm_chain.run(query=query, summaries=summaries)
    return summary_output, used_articles


# ✅ Outcome:
# I’ve now fully connected LangChain to Groq’s LLM and NewsAPI.
# My tool can now fetch and summarize real-time news on any topic — politics, tech, finance, sports, and more —
# using smart prompt templates and chains for accurate, readable summaries.
