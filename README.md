# 🎓 Nova Admissions AI

A smart, context-aware AI agent designed to streamline university admissions inquiries. Built with **Llama 3**, **Groq**, and **Streamlit**.

## 🌟 Key Features

* **🧠 Conversational Memory:** Remembers user context (e.g., previous questions, student ID) using a SQLite storage layer.
* **🛡️ Robust Guardrails:** Prevents "Scope Creep" by strictly limiting conversations to admissions topics only.
* **⚡ Real-Time Database Tools:** Instantly queries a SQL database to fetch live application status.
* **❤️ Emotional Intelligence:** Detects user sentiment (e.g., disappointment, joy) and responds with appropriate empathy or celebration.
* **✅ Hallucination Control:** Grounded advice logic prevents the agent from inventing fake university policies.

## 🛠️ Tech Stack

* **LLM Engine:** Llama 3.3 (via Groq API) for sub-second inference.
* **Framework:** Phidata (Agent orchestration).
* **Frontend:** Streamlit (Chat UI).
* **Database:** SQLite (Local student records).

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Durgaprasadpenumuru/admissions-ai-agent.git](https://github.com/Durgaprasadpenumuru/admissions-ai-agent.git)
    cd admissions-ai-agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your secrets:**
    * Create a `.env` file in the root folder.
    * Add your API key: `GROQ_API_KEY=your_key_here`

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

## 🧪 Test Data (For Demo)

Use these IDs to test different scenarios:
* `STU-1001`: **Accepted** (Trigger celebratory response)
* `STU-1002`: **Rejected** (Trigger empathetic advice)
* `STU-1003`: **Pending** (Trigger informative status)


---
*Created by Durga Prasad*