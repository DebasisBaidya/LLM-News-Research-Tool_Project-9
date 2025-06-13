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
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient

# 📌 Task 1.1: Load Environment Variables
# 🔐 Load API keys securely from .env or Streamlit Secrets
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

# 📌 Task 2.1: Initialize the Language Model
# 🧠 Connecting to Groq's LLaMA3 model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# 📌 Task 3.1: Design Prompt Template
# ✏️ This prompt ensures clear, fact-based summaries without fluff
enhanced_template = """
You are an intelligent and strictly factual AI news summarizer.

Given a user query and a set of real-time news article excerpts,
generate an accurate, concise summary of the situation.

✅ Summary Guidelines:
• Be strictly factual and free of bias
• Cover key developments and details
• Provide 4 to 6 bullet points only
• Use the • bullet symbol consistently
• Avoid restating the query or adding an intro/outro
• NEVER invent or speculate — rely strictly on article data

---

📝 User Query:
{query}

📰 News Article Content:
{summaries}

---

📌 Provide only the final bullet-point summary below:
"""

# 📌 Task 3.1.2: Compile Prompt Template
prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])

# 🔗 Create LLMChain with model and prompt
llm_chain = LLMChain(prompt=prompt, llm=llm)

# 📌 Task 3.2: Setup NewsAPI
# 🌐 Fetch news articles via keyword search
newsapi = NewsApiClient(api_key=news_api_key)

def get_news_articles(query):
    articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=10)
    return articles.get("articles", [])

# 📌 Task 3.2.1: Combine article content into a string
# 🧾 Extract description or content from each article
def summarize_articles(articles):
    return ' '.join(
        article.get('description') or article.get('content') or ''
        for article in articles
    )

# 📌 Task 3.3: Summarization Entry Point
# 🧠 Return a summary and metadata for use in the UI
def get_summary(query):
    articles = get_news_articles(query)
    summaries = summarize_articles(articles)

    if not summaries.strip():
        return "⚠️ No content found to summarize. Try another topic.", []

    used_articles = [a for a in articles if a.get('description') or a.get('content')]
    summary_output = llm_chain.run(query=query, summaries=summaries)

    return summary_output, used_articles



# ✅ Outcome:
# I’ve now fully connected LangChain to Groq’s LLM and NewsAPI.
# My tool can now fetch and summarize real-time news on any topic — politics, tech, finance, sports, and more —
# using smart prompt templates and chains for accurate, readable summaries.
