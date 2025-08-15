

### **▶️ Demo**

_A live demonstration of the Alternex Voice Agent in action._

\<div align="center"\>
\<img src="[https://i.imgur.com/your-gif-url.gif](https://www.google.com/search?q=https://i.imgur.com/your-gif-url.gif)" alt="Alternex Voice Agent Demo"/\>
\</div\>

---

### **✨ Features**

Alternex is designed to provide a seamless and intuitive conversational experience.

- **🗣️ Voice-First Interaction**: Simply tap the microphone, speak your query, and receive a spoken response in real-time.
- **🧠 Conversational Memory**: The agent remembers the context of your current conversation, allowing for natural follow-up questions.
- **🚀 High-Performance Backend**: Built with **FastAPI**, ensuring fast, asynchronous request handling.
- **🎨 Modern UI**: A clean and responsive user interface that looks great on any device.
- **🔒 Secure API Handling**: API keys are kept secure and out of version control using a simple and effective configuration method.
- **🏗️ Modular & Scalable**: The backend is organized into logical services, making it easy to maintain and extend.

---

### **🛠️ Tech Stack**

This project leverages a modern stack of technologies for a robust and efficient application.

| Area            | Technology                                                                                                      |
| :-------------- | :-------------------------------------------------------------------------------------------------------------- |
| **Backend**     |                                                                                                                 |
| **Frontend**    |                                                                                                                 |
| **AI Services** | **Google Gemini** (Language Model) \<br/\> **AssemblyAI** (Speech-to-Text) \<br/\> **Murf AI** (Text-to-Speech) |

---

### **📂 Project Structure**

The project is organized with a clean separation of concerns.

```
/voice-agent-project/
│
├── backend/
│   ├── .gitignore
│   ├── main.py             # FastAPI server logic
│   ├── config.py           # Secure API key storage (ignored by Git)
│   ├── requirements.txt    # Python dependencies
│   │
│   ├── services/           # Modular services for third-party APIs
│   │   ├── __init__.py
│   │   ├── llm.py          # Handles Gemini LLM logic
│   │   ├── stt.py          # Handles AssemblyAI STT logic
│   │   └── tts.py          # Handles Murf AI TTS logic
│   │
│   ├── static/
│   │   ├── fallback.mp3
│   │   └── script.js
│   │
│   └── templates/
│       └── index.html
│
└── README.md
```

---

### **🚀 Getting Started**

Follow these steps to get the Alternex Voice Agent running on your local machine.

#### **Prerequisites**

- Python 3.8+
- An IDE like VS Code

#### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name/backend
```

#### **2. Set Up the Backend**

- **Create a virtual environment:**
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
- **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

#### **3. Configure API Keys**

- Create a file named `config.py` inside the `backend` directory.
- **Important**: The `.gitignore` file is already set up to prevent `config.py` from being uploaded to GitHub, keeping your keys safe.
- Copy the following into `config.py` and add your secret keys:
  ```python
  # backend/config.py
  MURF_API_KEY = "your_murf_api_key"
  ASSEMBLYAI_API_KEY = "your_assemblyai_api_key"
  GEMINI_API_KEY = "your_gemini_api_key"
  ```

#### **4. Run the Application**

- Start the FastAPI server:
  ```bash
  uvicorn main:app --reload
  ```
- Open your browser and navigate to `http://127.0.0.1:8000`.

---

### **👨‍💻 About the Author**

This project was developed by **Sibsankar Samal**. I am a passionate developer with a love for building innovative and user-friendly applications.

---

### **📫 Connect with Me**

Feel free to reach out and connect\!

<p align="left">
  <a href="https://www.linkedin.com/in/sibsankarsamal" target="_blank">
    <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://www.instagram.com/ft.shivv/" target="_blank">
    <img alt="Instagram" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" />
  </a>
  <a href="https://sibsankarportfolio.netlify.app" target="_blank">
    <img alt="Portfolio" src="https://img.shields.io/badge/My_Portfolio-282C34?style=for-the-badge&logo=suckless&logoColor=white" />
  </a>
</p>
