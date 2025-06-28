# 🧠 LLM Project: News Research Tool  
🔍 Real-Time AI-Powered News Summarizer using LangChain, Groq & NewsAPI

[![Streamlit App](https://img.shields.io/badge/🚀%20Live%20App-Open%20in%20Browser-brightgreen?style=for-the-badge)](https://llm-news-research-tool-debasisbaidya.streamlit.app/)
[![🎬 Demo Video](https://img.shields.io/badge/🎬%20Demo-Watch%20Now-red?style=for-the-badge)](https://youtu.be/s5lrqv6oAR4)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge)](https://www.python.org/downloads/release/python-3130a1/)
[![LangChain](https://img.shields.io/badge/LangChain%20+%20Groq-News%20API-orange?style=for-the-badge)](https://www.langchain.com/)

</div>

- 🔗 **Live App**: [Click here to try the app](https://llm-news-research-tool-debasisbaidya.streamlit.app/)
- 🎬 **Demo Video**: [Watch the demo video](https://youtu.be/s5lrqv6oAR4)

---

## 📌 Project Overview

The **News Research Tool** is an interactive web app that allows users to:

- 🔍 Search for any trending topic (e.g. "AI in healthcare", "Global warming")
- 📡 Fetch real-time articles using **NewsAPI**
- 🧠 Generate crisp, point-wise summaries using **Groq's LLaMA3** via **LangChain**
- 🖥️ Use a simple, secure **Streamlit interface**
- 📥 Download summaries as `.txt` or `.pdf`
- 📚 See previous query history

---

## 🚀 Key Features

- 🔐 Login-required access (username/password)
- 🔍 Real-time topic-based news search
- 🧠 Short bullet-style summarization using LLM
- 📁 Export summaries in multiple formats
- 💡 Suggestion buttons for quick start
- 🕓 Past 5-query history preview

---

## 🧰 Built With

| Component       | Purpose                           |
|------------------|-----------------------------------|
| 🐍 Python 3.13    | Base language                     |
| 🧠 Groq (LLaMA3)  | Fast LLM summarization            |
| 🦜 LangChain      | LLM orchestration logic           |
| 🌐 NewsAPI        | Real-time news data               |
| 🌿 Streamlit      | Web app frontend                  |
| 🧾 ReportLab      | PDF export generation             |
| 🔐 python-dotenv  | Secure API key loading            |

---

## 📁 File Structure

```

├── app.py               # Streamlit interface
├── langchain_config.py  # LLM + NewsAPI setup
├── requirements.txt     # Python dependencies
├── README.md            # This documentation

```

## 📒 Note:
- API keys (GROQ_API_KEY and NEWS_API_KEY) are securely stored in Streamlit Secrets rather than in a .env file, unlike during development in PyCharm.
- This is to prevent exposure on GitHub, where keys in .env files can be automatically revoked by GitHub or Groq for security reasons.


---

## 📸 App Preview

> _Screenshot of Log In & Main App Page_

<div style="display: flex; flex-direction: column; align-items: center; gap: 20px;">

  <!-- Screenshot 1: smaller and centered -->
  <img src="Log-In Authentication.png" alt="Screenshot 1" style="width: 80%;"/>

  <!-- Screenshot 2: larger and also centered -->
  <img src="Main App Page.png" alt="Screenshot 2" style="width: 80%;" />

</div>

---

## 🎬 Demo Video

> _How the App Works_

🎥 [Watch Demo](https://youtu.be/s5lrqv6oAR4))

---

## 🙋‍♂️ About Me

**Debasis Baidya**  
Senior MIS | Data Science Intern  
✅ Automated 80%+ of manual processes at my workplace  
📊 Skilled in Python, Power BI, SQL, Google Apps Script, ML, DL, NLP  
<p align="left">
  📫 <strong>Connect with me:</strong>&nbsp;

  <a href="https://www.linkedin.com/in/debasisbaidya">
    <img src="https://img.shields.io/badge/LinkedIn-View_Profile-blue?logo=linkedin&logoColor=white" />
  </a>

  <a href="mailto:speak2debasis@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-Mail_Me-red?logo=gmail&logoColor=white" />
  </a>

  <a href="https://api.whatsapp.com/send?phone=918013316086&text=Hi%20Debasis!">
    <img src="https://img.shields.io/badge/WhatsApp-Message-green?logo=whatsapp&logoColor=white" />
  </a>
</p>

---

⭐ If you found this project helpful, don’t forget to **star this repo** and stay connected!

---

## 🧠 Powered By

- [LangChain](https://www.langchain.com/)  
- [Groq API](https://console.groq.com/)  
- [NewsAPI](https://newsapi.org/)  
- [Streamlit](https://streamlit.io/)

> ✨ Built for smart research and crisp insights using real-time LLMs.
