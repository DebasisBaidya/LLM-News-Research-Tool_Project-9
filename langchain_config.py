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

# 📌 Task 1.3: is in 'Streamlit Secret TOML' file

# ✅ Phase 2: LangChain Configuration using Groq API
# ----------------------------------------------------

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient

# ✅ Loading environment variables from .env file
#load_dotenv()

# ✅ Access secrets via st.secrets or os.environ
groq_api_key = st.secrets["GROQ_API_KEY"]
news_api_key = st.secrets["NEWS_API_KEY"]

# ✅ Initializing Groq-based LLM
# I’m connecting to Groq's LLaMA3 model (powerful, fast, free to use)
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192")

# ✅ 🧠 Prompt Template with Crisp Bullet Output
initial_template = """
🗞️ **Latest News Summary on: {query}**

You are a smart and concise AI assistant summarizing breaking or trending news. Based on the topic, generate a short, factual overview in 3 to 5 bullet points.

🎯 Format: Bullet points only  
✅ Tone: Crisp, neutral, informative  
🚫 Avoid: Repetition, filler, and vague language

Provide the summary below:

- 
"""

# ✅ Creating a prompt object with input variable 'query'
prompt = PromptTemplate(template=initial_template, input_variables=["query"])

# ✅ Setting up LangChain LLMChain to connect the prompt and Groq LLM
llm_chain = LLMChain(prompt=prompt, llm=llm)

# ✅ Initializing NewsAPI client to fetch real-time news articles
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def get_news_articles(query):
    # ✅ Using NewsAPI to fetch relevant news articles based on user input
    articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
    return articles['articles']

def summarize_articles(articles):
    # ✅ Extracting article descriptions (if present) to create input for summarization
    summaries = [article['description'] or '' for article in articles if article.get('description')]
    return ' '.join(summaries)

def get_summary(query):
    # ✅ Main controller: fetches news and feeds them into the LLM for summarization
    articles = get_news_articles(query)
    summaries = summarize_articles(articles)
    return llm_chain.run(query=query, summaries=summaries)

# ✅ Enhanced Prompt Template for smarter summarization using actual content
# This helps the LLM generate more context-aware, high-quality summaries
enhanced_template = """
You are an intelligent AI news summarizer. Based on the given user query and the collected summaries from multiple articles,
generate a clear, unbiased, and informative overview of the topic. Ensure the summary is digestible and reflects the key points covered by the news.

Query: {query}
Summaries: {summaries}
"""

# ✅ Rebuilding the LLMChain with improved prompt and both inputs: query + summaries
enhanced_prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])
llm_chain = LLMChain(prompt=enhanced_prompt, llm=llm)


# ✅ Outcome:
# I’ve now fully connected LangChain to Groq’s LLM and NewsAPI.
# My tool can now fetch and summarize real-time news on any topic — politics, tech, finance, sports, and more —
# using smart prompt templates and chains for accurate, readable summaries.
