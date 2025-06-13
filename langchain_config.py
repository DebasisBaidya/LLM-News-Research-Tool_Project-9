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

# 🔐 Loading API keys from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]
news_api_key = st.secrets["NEWS_API_KEY"]

# ✅ Initializing Groq LLM with LLaMA3
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# ✅ Creating a richer, detailed prompt for factual AI summarization
enhanced_template = """
You are a highly factual AI news summarizer.

Using the provided real-time news article content and user query, generate a clear and informative summary of the current situation.

✅ The summary should:
- Be factually accurate and unbiased
- Contain 4 to 6 bullet points
- Mention key details: what, when, where, who, impact
- Use professional, news-style language

Do NOT make anything up — base everything strictly on the provided content.

---

📝 User Query:
{query}

📰 News Article Content:
{summaries}

---

📌 Provide the final bullet-point summary below:
"""

# Creating prompt template
enhanced_prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])

# Creating the LLM chain
llm_chain = LLMChain(prompt=enhanced_prompt, llm=llm)

# ✅ Initializing NewsAPI client
newsapi = NewsApiClient(api_key=news_api_key)

# ✅ Fetching news articles using query
def get_news_articles(query):
    articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=10)
    if not articles['articles']:
        st.warning("⚠️ No current articles found for this query.")
    return articles['articles']

# ✅ Extracting usable summaries from articles
def summarize_articles(articles):
    summaries = [
        article.get('description') or article.get('content') or ''
        for article in articles if article.get('description') or article.get('content')
    ]
    return ' '.join(summaries)

# ✅ Final function to display metadata and run summarization
def get_summary(query):
    articles = get_news_articles(query)
    summaries = summarize_articles(articles)

    if not summaries.strip():
        st.error("❌ No summary content could be extracted.")
        return "⚠️ No content found to summarize. Try another topic."

    # 📰 Show metadata of articles used
    used_articles = [article for article in articles if article.get('description') or article.get('content')]
    st.markdown("### 📰 Articles Used for Summary:")

    for i, article in enumerate(used_articles, 1):
        title = article.get("title", "No Title Found")
        source = article.get("source", {}).get("name", "Unknown Source")
        published = article.get("publishedAt", "Unknown Date").split("T")[0]
        url = article.get("url", "#")
        st.markdown(f"- {i}. **{title}**  \n📅 {published} | 🏷️ {source}  \n🔗 [Read More]({url})")

    # ✅ Show summary metadata
    sentence_count = len([s for s in summaries.split('.') if s.strip()])
    st.markdown(f"✅ **Summary extracted from {len(used_articles)} article(s) with approx. {sentence_count} sentence(s).**")

    # 🤖 Return LLM-generated summary
    return llm_chain.run(query=query, summaries=summaries)


# ✅ Outcome:
# I’ve now fully connected LangChain to Groq’s LLM and NewsAPI.
# My tool can now fetch and summarize real-time news on any topic — politics, tech, finance, sports, and more —
# using smart prompt templates and chains for accurate, readable summaries.
