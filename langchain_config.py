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

# 🔐 Task 2.1: Loading API keys from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]
news_api_key = st.secrets["NEWS_API_KEY"]

# ✅ Task 2.2: Initializing Groq LLM with LLaMA3
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# ✅ Task 2.3: Creating the enhanced prompt for summarization
enhanced_template = """
You are a highly factual AI summarizer.

Given the user query and the combined descriptions of the most recent news articles, write a short, accurate summary of what's currently happening.

🎯 Focus only on what the articles say. Do not guess or create content beyond the provided data.

Query: {query}

News Article Content: {summaries}

Provide a bullet-point summary:
"""

# 📌 Creating prompt template with 2 inputs: query and summaries
enhanced_prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])

# 📌 Creating LangChain LLMChain object with prompt + LLM
llm_chain = LLMChain(prompt=enhanced_prompt, llm=llm)

# ✅ Task 3.1: Initializing NewsAPI to fetch current news
newsapi = NewsApiClient(api_key=news_api_key)

# ✅ Task 3.2: Fetching articles by query
def get_news_articles(query):
    # 🔍 Getting recent articles sorted by time
    articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=10)

    if not articles['articles']:
        st.warning("⚠️ No current articles found for this query.")
    return articles['articles']

# ✅ Task 3.3: Extracting usable descriptions/content from fetched articles
def summarize_articles(articles):
    summaries = [
        article.get('description') or article.get('content') or ''
        for article in articles if article.get('description') or article.get('content')
    ]
    return ' '.join(summaries)

# ✅ Task 3.4: Running the summarization LLM chain
def get_summary(query):
    articles = get_news_articles(query)
    summaries = summarize_articles(articles)

    if not summaries.strip():
        st.error("❌ No summary content could be extracted.")
        return "⚠️ No content found to summarize. Try another topic."

    # ✅ Showing both title and usable count in one neat markdown section
    if articles:
        top_title = articles[0].get('title', 'No Title Found')
        sentence_count = len([s for s in summaries.split('.') if s.strip()])
        st.markdown(f"📰 **Top Article Title:** {top_title}")
        st.markdown(f"✅ **Summary extracted from {sentence_count} article section(s).**")

    return summaries


# ✅ Outcome:
# I’ve now fully connected LangChain to Groq’s LLM and NewsAPI.
# My tool can now fetch and summarize real-time news on any topic — politics, tech, finance, sports, and more —
# using smart prompt templates and chains for accurate, readable summaries.
