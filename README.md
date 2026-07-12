# 🌿 Ayurvedic Medicine AI — Grandma Anong's Traditional Remedies

A **Streamlit-powered chat interface** that connects to a **RAG-based watsonx Orchestrate agent** — bringing Grandma Anong's five-generation Ayurvedic knowledge to anyone with a link.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.59-red)
![IBM Cloud](https://img.shields.io/badge/IBM%20Cloud-watsonx%20Orchestrate-blueviolet)

---

## 🌟 About the Agent

This AI assistant is built on **proprietary Ayurvedic knowledge** from Grandma Anong's wellness center in Kerala, India — authentic herbal remedies and traditional healing practices passed down through **five generations**.

The knowledge is powered by a **RAG (Retrieval-Augmented Generation)** pipeline using watsonx Orchestrate, which retrieves from a document store containing the family's unique herbal formulations and treatment methods that are not documented in any public books, websites, or other wellness centers.

### What it can help with:
- **🤧 Cold & Cough** — Ginger, tulsi, honey-based remedies
- **🤢 Indigestion** — Cumin, ginger, lemon formulations
- **🤕 Headaches** — Traditional herbal preparations
- **🩹 Skin Irritations** — Neem, turmeric-based treatments
- **🔥 Fever** — Herbal decoctions and recipes
- **💪 Minor Aches** — Ayurvedic oil and paste preparations

All remedies use **everyday kitchen ingredients** with clear step-by-step preparation instructions and dosage guidance.

---

## ✨ Features

- **💬 Chat interface** — Clean, intuitive Streamlit UI for conversing with the Ayurvedic agent
- **📚 RAG-powered answers** — Retrieves from Grandma Anong's proprietary document store
- **🔐 IAM authentication** — Automatic token management via IBM Cloud API key
- **🔄 Conversation tracking** — Maintains context across messages using thread IDs
- **🌱 Quick remedy prompts** — One-click buttons for common health concerns
- **🧹 New Conversation** — Reset the chat with one click
- **☁️ Docker-ready** — Deploy to IBM Cloud Code Engine or any container platform

---

## 📋 Prerequisites

| Requirement | Details |
|-------------|---------|
| IBM Cloud Account | [Sign up free](https://cloud.ibm.com/registration) |
| watsonx Orchestrate Instance | [Create one](https://cloud.ibm.com/catalog/services/watsonx-orchestrate) |
| IBM Cloud API Key | [Create here](https://cloud.ibm.com/iam/apikeys) |
| Python 3.11+ | Local development |

---

## 🚀 Quick Start (Local)

### 1. Clone

```bash
git clone https://github.com/PRATIKKADU53/RAG-Based-Traditional-Ayurvedic-Medicine-Ai-Agent.git
cd RAG-Based-Traditional-Ayurvedic-Medicine-Ai-Agent
```

### 2. Set Up Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your credentials
```

Your `.env` file should look like:

```env
ORCHESTRATE_API_KEY="your-ibm-cloud-api-key"
ORCHESTRATE_INSTANCE_ID="your-orchestrate-instance-id"
ORCHESTRATE_REGION="us-south"
ORCHESTRATE_AGENT_ID="your-agent-id"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser and start asking about Ayurvedic remedies!

---

## ☁️ Deploy to IBM Cloud Code Engine (Web Console)

### Step 1: Create a Code Engine Project
1. Go to [IBM Cloud Code Engine](https://cloud.ibm.com/codeengine/overview)
2. Click **"Start creating"** → **"Create project"**
3. Name it (e.g., `ayurvedic-chat-app`) and create

### Step 2: Create an Application
1. Inside your project, click **"Application"** → **"Create application"**

| Setting | Value |
|---------|-------|
| **Container source** | Build from repository |
| **Repository URL** | `https://github.com/PRATIKKADU53/RAG-Based-Traditional-Ayurvedic-Medicine-Ai-Agent` |
| **Branch** | `main` |
| **Dockerfile** | Checked (use `Dockerfile`) |
| **Port** | `8501` |
| **CPU / Memory** | `0.5 vCPU` / `1 GB` |
| **Min scale** | `0` (scales to zero — free when idle) |
| **Max scale** | `1` |

### Step 3: Add Environment Variables
Add these under **Environment variables** (mark as **secret/protected**):

| Name | Value |
|------|-------|
| `ORCHESTRATE_API_KEY` | Your IBM Cloud API key |
| `ORCHESTRATE_INSTANCE_ID` | Your watsonx Orchestrate instance ID |
| `ORCHESTRATE_REGION` | `us-south` |
| `ORCHESTRATE_AGENT_ID` | Your agent ID |

### Step 4: Deploy
Click **"Create"** and wait ~3-5 minutes. You'll get a public URL like:

```
https://ayurvedic-chat-app.abc123.codeengine.appdomain.cloud
```

Share this link with anyone — friends, faculty, or clients!

---

## 🔧 Configuration Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ORCHESTRATE_API_KEY` | ✅ Yes | — | IBM Cloud API key |
| `ORCHESTRATE_INSTANCE_ID` | ✅ Yes | — | watsonx Orchestrate instance GUID |
| `ORCHESTRATE_REGION` | ❌ No | `us-south` | API region |
| `ORCHESTRATE_AGENT_ID` | ✅ Yes | — | Your Ayurvedic agent ID |

---

## 📁 Project Structure

```
├── app.py                 # Streamlit chat application
├── requirements.txt       # Python dependencies
├── .env                   # Credentials (gitignored — never commit)
├── .env.example           # Template for env vars
├── Dockerfile             # Container definition for Code Engine
├── .gitignore
└── README.md              # This file
```

---

## 🤝 How It Works

1. The app authenticates with **IBM Cloud IAM** using your API key
2. Your message is sent to the **watsonx Orchestrate Runs API**
3. The **RAG agent** retrieves relevant knowledge from Grandma Anong's proprietary document store
4. An LLM synthesizes the response with the retrieved context
5. The remedy is displayed in a clean chat interface with conversation history

---

## 📝 Notes

- Credentials stay in your `.env` file or Code Engine secrets — **never committed to Git**
- Conversation context is maintained via thread IDs in your browser session
- Click **New Conversation** anytime to start fresh
- The knowledge base contains **proprietary family remedies** not available in public sources
- For best results, describe your symptoms clearly and mention any relevant ingredients you have on hand

---

## 📄 License

MIT
