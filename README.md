# 📰 Equity Research News Tool

An interactive AI-powered tool that fetches and summarizes the latest news articles in real-time using **NewsAPI** and **Groq’s LLM (via LangChain)**. Built with a simple **Streamlit interface**, this tool is designed to assist equity research analysts in quickly understanding market-moving news.

---

## 🚀 Features

- 🔍 Search and summarize live news articles based on any topic or company  
- 🧠 Uses **Groq’s Mixtral LLM** for smart, human-like summarization  
- 📡 Fetches real-time articles via **NewsAPI**  
- 🖥️ Intuitive Streamlit interface – No technical knowledge required  

---

## 🧰 Tech Stack

- 🦜 LangChain  
- 🧠 Groq LLM (Mixtral)  
- 🌐 NewsAPI  
- 🌿 Streamlit  
- 🔐 python-dotenv  

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/news-research-tool.git
cd news-research-tool
```

### 2. Install Dependencies

```bash
pip install langchain streamlit newsapi-python groq python-dotenv
```

### 3. Get API Keys

- 🔑 [Groq API Key](https://console.groq.com/keys)  
- 🔑 [NewsAPI Key](https://newsapi.org/)  

### 4. Create `.env` File

Create a `.env` file in the project root and add:

```
GROQ_API_KEY=your-groq-api-key
NEWS_API_KEY=your-newsapi-key
```

---

## ▶️ How to Run the App

```bash
streamlit run app.py
```

---

## 📸 App Interface

- **Input Box** – Enter your topic or query (e.g., “Tesla stock”, “Artificial Intelligence”)  
- **Button** – Click "Get News Summary"  
- **Output** – AI-generated concise news summary displayed below  

---

## 🧠 Behind the Scenes

- The app fetches news from **NewsAPI**  
- Extracts key content from article descriptions  
- Sends it to **Groq LLM via LangChain** with a tailored prompt  
- Displays the intelligent, AI-generated summary on-screen  

---

## 📁 Project Structure

```
├── app.py               # Streamlit front-end  
├── langchain_config.py  # LangChain + Groq + NewsAPI integration  
├── .env                 # API keys (excluded from Git)  
└── README.md            # Project documentation  
```

---

## 👨‍💻 Author

**Debasis Baidya**  
🔗 [LinkedIn](https://www.linkedin.com/in/debasisbaidya)

---

## 📄 License

This project is licensed under the MIT License.
