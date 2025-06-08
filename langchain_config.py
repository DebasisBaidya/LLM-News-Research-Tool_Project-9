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
# I’m connecting to Groq's Mixtral model which is powerful and free to use
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192")

# ✅ Setting up the prompt template (Basic for Task 2.2)
initial_template = """
You are an AI assistant helping an equity research analyst. Given the following query, summarize the most relevant news articles.

Query: {query}
"""

prompt = PromptTemplate(template=initial_template, input_variables=["query"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

# ✅ Initializing NewsAPI client to fetch real-time news articles
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def get_news_articles(query):
    # I’m calling NewsAPI to get relevant articles based on the input query
    articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
    return articles['articles']

def summarize_articles(articles):
    # I’m extracting descriptions from each article to form a combined summary input
    summaries = [article['description'] or '' for article in articles]
    return ' '.join(summaries)

def get_summary(query):
    # This function is calling both fetching and summarizing in one flow
    articles = get_news_articles(query)
    summary = summarize_articles(articles)
    return summary

# ✅ Enhanced Prompt Template for use with article summaries
# This helps the model generate more specific and accurate insights based on actual news context
enhanced_template = """
You are an AI assistant helping an equity research analyst. Given the following query and the provided news article summaries, provide an overall summary.

Query: {query}
Summaries: {summaries}
"""

enhanced_prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])
llm_chain = LLMChain(prompt=enhanced_prompt, llm=llm)

# ✅ Outcome:
# I’ve now fully connected LangChain to Groq’s LLM and NewsAPI. My tool is ready to process live news data
# and summarize them smartly based on user queries using prompt templates and chains.
