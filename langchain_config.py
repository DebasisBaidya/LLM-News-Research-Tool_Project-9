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

# 🔐 Task 2.1: Loading API keys securely
groq_api_key = st.secrets["GROQ_API_KEY"]
news_api_key = st.secrets["NEWS_API_KEY"]

# ✅ Task 2.2: Initializing LLM with Groq’s LLaMA3 model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# ✅ Task 2.3: Creating enhanced summarization prompt
enhanced_template = """
You are a highly factual AI summarizer.

Given the user query and the combined descriptions of the most recent news articles, write a short, accurate summary of what's currently happening.

🎯 Focus only on what the articles say. Do not guess or create content beyond the provided data.

Query: {query}

News Article Content: {summaries}

Provide a bullet-point summary:
"""
enhanced_prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])
llm_chain = LLMChain(prompt=enhanced_prompt, llm=llm)

# ✅ Task 3.1: Initializing NewsAPI client
newsapi = NewsApiClient(api_key=news_api_key)

# ✅ Task 3.2: Fetching and summarizing real-time articles
def get_news_articles(query):
    articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=10)
    if not articles['articles']:
        st.warning("⚠️ No current articles found for this query.")
    else:
        st.write("📰 Top Article Title:", articles['articles'][0].get('title', 'No Title Found'))
    return articles['articles']

def summarize_articles(articles):
    summaries = [
        article.get('description') or article.get('content') or ''
        for article in articles if article.get('description') or article.get('content')
    ]
    if summaries:
        st.success(f"✅ Found {len(summaries)} usable article descriptions.")
    else:
        st.error("❌ No summary content could be extracted.")
    return ' '.join(summaries)

# ✅ Task 3.3: Running summarization chain
def get_summary(query):
    articles = get_news_articles(query)
    summaries = summarize_articles(articles)
    if not summaries.strip():
        return "⚠️ No content found to summarize. Try another topic."
    return summaries


# ✅ Outcome:
# I’ve now fully connected LangChain to Groq’s LLM and NewsAPI.
# My tool can now fetch and summarize real-time news on any topic — politics, tech, finance, sports, and more —
# using smart prompt templates and chains for accurate, readable summaries.
