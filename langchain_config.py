# ✅ Phase 2: LangChain Configuration using Groq API
# ----------------------------------------------------

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient

# ✅ Loading environment variables from .env file
load_dotenv()

# ✅ Setting up API keys securely using os.getenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ✅ Initializing Groq-based LLM
# I’m connecting to Groq's LLaMA3 model (powerful, fast, free to use)
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192")

# ✅ Updated Prompt Template for general-purpose news summarization
initial_template = """
You are an intelligent AI assistant that summarizes the latest news on any topic. 
Given a user query, gather and generate a brief, clear, and informative overview of recent news articles on that topic.

Query: {query}
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
