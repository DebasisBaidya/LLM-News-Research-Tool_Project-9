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

# 📌 I am importing necessary modules and loading environment variables

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient

# 🔐 I am using Streamlit secrets to securely access API keys
groq_api_key = st.secrets["GROQ_API_KEY"]
news_api_key = st.secrets["NEWS_API_KEY"]

# ✅ I am initializing the Groq-based LLM (LLaMA3)
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# ✅ I am defining an enhanced prompt template for better summaries
enhanced_template = """
You are a highly factual AI summarizer.

Given the user query and the combined descriptions of the most recent news articles, write a short, accurate summary of what's currently happening.

🎯 Focus only on what the articles say. Do not guess or create content beyond the provided data.

Query: {query}

News Article Content: {summaries}

Provide a bullet-point summary:
"""

# ✅ I am creating a prompt object using both query and summaries as input variables
enhanced_prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])

# ✅ I am creating an LLMChain that connects the prompt to the model
llm_chain = LLMChain(prompt=enhanced_prompt, llm=llm)

# ✅ I am initializing NewsAPI client to fetch live news articles
newsapi = NewsApiClient(api_key=news_api_key)

# ✅ I am defining a function to fetch current articles based on the user's query
def get_news_articles(query):
    # 🔍 I am requesting the latest articles sorted by publication date
    articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=10)

    # ✅ I am showing a warning if no articles are found
    if not articles['articles']:
        st.warning("⚠️ No current articles found for this query. Try with another trending topic.")

    # 🧪 I am printing the title of the first article for confirmation
    if articles['articles']:
        st.write("📰 Top Article Title:", articles['articles'][0].get('title', 'No Title Found'))

    return articles['articles']

# ✅ I am defining a function to extract usable content from each article
def summarize_articles(articles):
    # 🧾 I am extracting 'description' or 'content' from each article
    summaries = [
        article.get('description') or article.get('content') or ''
        for article in articles
        if article.get('description') or article.get('content')
    ]

    # ⚠️ I am checking and warning if summaries are still empty
    if not summaries:
        st.warning("⚠️ No usable content found in fetched articles.")

    return ' '.join(summaries)

# ✅ I am defining the main function that combines all steps to generate the final summary
def get_summary(query):
    # 📰 I am fetching news articles for the given query
    articles = get_news_articles(query)

    # 🧾 I am combining descriptions or content into one long text
    summaries = summarize_articles(articles)

    # 🤖 I am running the enhanced prompt through the LLM to get the summary
    return llm_chain.run(query=query, summaries=summaries)


# ✅ Outcome:
# I’ve now fully connected LangChain to Groq’s LLM and NewsAPI.
# My tool can now fetch and summarize real-time news on any topic — politics, tech, finance, sports, and more —
# using smart prompt templates and chains for accurate, readable summaries.
