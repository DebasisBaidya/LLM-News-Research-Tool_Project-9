# ✅ Phase 1 → Phase 3: Environment Setup + LangChain + Summarization Logic

import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient

# ✅ Phase 1: API Integration
# 🔐 I’m loading API keys securely from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]
news_api_key = st.secrets["NEWS_API_KEY"]

# ✅ Phase 2: Model Initialization
# 🧠 I’m initializing Groq’s LLaMA3 model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# ✅ Phase 3.1: Enhanced Prompt Template for Detailed Summaries
enhanced_template = """
You are a highly factual AI news summarizer.

Using the provided real-time news article content and user query, generate a clear and informative summary of the current situation.

✅ The summary should:
- Be factually accurate and unbiased
- Contain 4 to 6 bullet points
- Each point must start with •
- No titles, no mainpoint-subpoint format, no headings
- Just pure bullet points with short paragraph breaks
- Do NOT include intro or outro lines

Only base the summary on the article content. Do not fabricate or assume anything.

---

📝 User Query:
{query}

📰 News Article Content:
{summaries}

---

📌 Provide the final formatted bullet-point summary below using •:
"""

# 🎯 Prompt template with required input variables
enhanced_prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])

# 🔗 I’m linking the prompt and model using LLMChain
llm_chain = LLMChain(prompt=enhanced_prompt, llm=llm)

# ✅ Phase 3.2: News Fetching
# 📡 I’m initializing NewsAPI client
newsapi = NewsApiClient(api_key=news_api_key)

# 🔍 I’m fetching relevant articles using the user query
def get_news_articles(query):
    articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=10)
    if not articles['articles']:
        st.warning("⚠️ No current articles found for this query.")
    return articles['articles']

# 🧾 I’m extracting summaries from article descriptions or content
def summarize_articles(articles):
    summaries = [
        article.get('description') or article.get('content') or ''
        for article in articles if article.get('description') or article.get('content')
    ]
    return ' '.join(summaries)

# ✅ Phase 3.3: Final Summary Output
# 📋 I’m generating the summary and returning top 3 articles for display
def get_summary(query):
    articles = get_news_articles(query)
    summaries = summarize_articles(articles)

    if not summaries.strip():
        st.error("❌ No summary content could be extracted.")
        return "⚠️ No content found to summarize. Try another topic.", []

    used_articles = [article for article in articles if article.get('description') or article.get('content')]

    # 🤖 I’m generating the AI bullet-point summary
    summary_output = llm_chain.run(query=query, summaries=summaries)

    return summary_output, used_articles[:3]  # return only top 3 articles
