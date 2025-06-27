# ✅ Phase 1: Environment Setup (Completed)
# -----------------------------------------------------
# 📌 Task 1.1: Install Required Libraries
# - Installing the essential Python libraries to handle LLM logic, UI, and news scraping.
# - The required libraries are: langchain, streamlit, newsapi-python, groq, langchain-groq, and python-dotenv

# ✅ Installation Command:
# pip install langchain streamlit newsapi-python groq langchain-groq python-dotenv

# 📌 Task 1.2: Obtain API Keys
# - Generating the required API keys to access Groq’s LLM and NewsAPI.
# - Getting Groq API key from: https://console.groq.com/keys
# - Getting NewsAPI key from: https://newsapi.org/

# 📌 Task 1.3: Store in 'Streamlit Secret TOML' file

# ✅ Phase 1 → Phase 3: Environment Setup + LangChain + Summarization Logic

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient

# 📌 Task 1.1: Loading API keys securely
# 🔐 Reading from environment variables or Streamlit secrets
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

# 📌 Task 2.1: Initializing the language model
# 🧠 Connecting to Groq's LLaMA3 model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# 📌 Task 3.1: Defining a detailed and improved prompt
# ✍️ Making sure the summary is fresh, relevant, and non-repetitive
enhanced_template = """
You are an intelligent and unbiased AI summarizer.

Your job is to summarize real-time news based on the provided articles and the user query.

Please keep in mind the following things:

✅ Begin with the actual incident — the first bullet must clearly state what happened, when, and where (exact place, date, and time). This is the strongest and most important point.
✅ Each bullet must present fresh, verified, and complete facts as stated in the article — include new developments, official statements, investigations, eyewitness details, and responses.
✅ Every bullet must start with a strong, unique, and concrete fact — no weak intros, vague phrasing, or repetition.
✅ Cover all core elements of the event:
→ What happened
→ When and where
→ Who was involved
→ How it unfolded
→ Impact or damage
→ Authorities' response
→ Public reaction (if any)
→ Ongoing investigation or follow-up actions
✅ Use a neutral, factual, and professional tone, similar to a newswire or briefing — avoid storytelling or emotion.
✅ Maintain clean output: use 5 to 8 bullets, each prefixed by "•", with no intro or summary outside the bullets.

❌ Do NOT include:
– Generic summaries
– Conclusions, opinions, or interpretations
– Emotional language or commentary
– Labels like “Top Story” or “Headline”
❌ Never invent or assume anything — if it’s not in the article, don’t include it.
⚠️ Strictly rely on the article content — do not fill gaps with speculation or outside context.

---

📝 User Query:
{query}

📰 News Article Content:
{summaries}

---

📌 Return only the final bullet-point summary below:
"""

# 📌 Task 3.1.2: Creating the prompt template with required input variables
prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])

# 🔗 Creating a LangChain that links the LLM and prompt
llm_chain = LLMChain(prompt=prompt, llm=llm)

# 📌 Task 3.2: Initializing NewsAPI for article fetching
# 🌐 Pulling real-time news results
newsapi = NewsApiClient(api_key=news_api_key)

def get_news_articles(query):
    return newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=10).get("articles", [])

# 📌 Task 3.2.1: Extracting usable text for the model
# 🧾 Combining content and description from each article
def summarize_articles(articles):
    return ' '.join(
        article.get('description') or article.get('content') or ''
        for article in articles
    )

# 📌 Task 3.3: Main entry point for summarization
# 🧠 Returning the summary output and top articles for UI rendering
def get_summary(query):
    articles = get_news_articles(query)
    summaries = summarize_articles(articles)

    if not summaries.strip():
        return "⚠️ No content found to summarize. Try another topic.", []

    used_articles = [a for a in articles if a.get('description') or a.get('content')]
    summary_output = llm_chain.run(query=query, summaries=summaries)

    return summary_output, used_articles


# ✅ Outcome:
# Now fully connected LangChain to Groq’s LLM and NewsAPI.
# The tool can now fetch and summarize real-time news on any topic — politics, tech, finance, sports, and more —
# using smart prompt templates and chains for accurate, readable summaries.
