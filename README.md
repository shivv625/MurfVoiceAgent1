<a href="https://www.linkedin.com/in/sibsankarsamal" target="_blank">
  <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>

# 🎙️ AI Voice Agent with React & FastAPI

Welcome to the AI Voice Agent project\! This is a modern, conversational AI built with a sleek React frontend and a powerful Python (FastAPI) backend. It's designed to be a seamless, voice-first experience, allowing users to have natural conversations with an AI that remembers the context of your chat.

_(Suggestion: Replace this with a screenshot of your running application for a great visual effect\!)_

---

## ✨ Features

- **Modern & Animated UI**: A beautiful, dark-themed user interface built with React and animated using Framer Motion for a smooth, professional feel.
- **Voice-First Interaction**: Click the microphone, speak your query, and get a voice response.
- **Conversational Memory**: The agent remembers the history of your current conversation, allowing for follow-up questions and contextual understanding.
- **Real-time Processing**: The application provides a seamless flow from your speech to the AI's response.
- **Robust Error Handling**: The agent gracefully handles potential API failures and provides clear feedback to the user.
- **Separated Frontend & Backend**: A professional monorepo structure that separates the UI (React) from the logic (FastAPI), making the project scalable and easy to maintain.

---

## 🚀 Tech Stack

This project uses a modern set of technologies for both the frontend and backend.

| Frontend          | Backend         | AI Services       |
| :---------------- | :-------------- | :---------------- |
| **React**         | **Python 3.8+** | **Google Gemini** |
| **Framer Motion** | **FastAPI**     | **AssemblyAI**    |
| **Tailwind CSS**  | **Uvicorn**     | **Murf AI**       |
| **JavaScript**    | **Requests**    |                   |

---

## 📂 Project Structure

The project is organized into two main directories: `backend` and `frontend`.

```
/voice-agent-project/
│
├── backend/
│   ├── main.py             # FastAPI server logic
│   ├── requirements.txt      # Python dependencies
│   └── static/
│       └── fallback.mp3    # Audio for error states
│
├── frontend/
│   ├── public/
│   │   └── index.html      # Main HTML shell for React
│   ├── src/
│   │   ├── App.js          # The main React component
│   │   ├── index.css       # Tailwind CSS styles
│   │   └── index.js        # React entry point
│   ├── package.json        # Frontend dependencies
│   └── ...                 # Other config files
│
└── README.md               # This file
```

---

## 🛠️ How to Run

To run this project, you will need to start two separate servers in two different terminals: one for the backend and one for the frontend.

### 1\. Backend Setup

First, navigate to the `backend` directory.

```bash
cd backend
```

Create a virtual environment and install the required Python packages.

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

**Important**: Before starting the server, you must have your API keys set up. The current `main.py` has them hardcoded for ease of use, but for production, you should use a `.env` file.

Run the FastAPI server.

```bash
uvicorn main:app --reload
```

Your backend will now be running at `http://127.0.0.1:8000`.

### 2\. Frontend Setup

Open a **new terminal** and navigate to the `frontend` directory.

```bash
cd frontend
```

Install the required Node.js packages.

```bash
npm install
```

Start the React development server.

```bash
npm start
```

Your browser should automatically open to `http://localhost:3000`. You can now interact with your new voice agent\!

---

## 🔑 API Keys

This project requires API keys from three services:

- **Murf AI** (Text-to-Speech)
- **AssemblyAI** (Speech-to-Text)
- **Google Gemini** (Language Model)

For simplicity, these keys are currently set directly in the `backend/main.py` file. For a production environment, it is highly recommended to create a `.env` file in the `backend` directory and load them using a library like `python-dotenv`.

**Example `backend/.env` file:**

```
MURF_API_KEY="your_murf_api_key"
ASSEMBLYAI_API_KEY="your_assemblyai_api_key"
GEMINI_API_KEY="your_gemini_api_key"
```

---

## 💡 Troubleshooting

- **CORS Errors**: If the frontend has trouble connecting to the backend, ensure the `CORSMiddleware` in `main.py` is correctly configured. The current setup allows all origins (`*`) for development.
- **`npm start` fails**: If you encounter errors like `Cannot find module`, delete the `node_modules` folder and the `package-lock.json` file in the `frontend` directory, then run `npm install` again.
- **Microphone Access**: Make sure you grant the browser permission to access your microphone when prompted.
