# 🤖 AI Assistant — IBM watsonx Orchestrate Chat

A Streamlit-powered chat interface that connects to **IBM watsonx Orchestrate** — turning your AI agents into a clean, conversational web app.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.59-red)
![IBM Cloud](https://img.shields.io/badge/IBM%20Cloud-watsonx%20Orchestrate-blueviolet)

---

## ✨ Features

- **💬 Chat interface** — Clean, intuitive Streamlit UI for conversing with your Orchestrate agents
- **🔐 IAM authentication** — Automatic token management via your IBM Cloud API key
- **🔄 Conversation tracking** — Maintains context across messages using `conversation_id`
- **🚀 Quick prompts** — One-click buttons for common questions
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

### 1. Clone & Navigate

```bash
cd my-orchestrate-app
```

### 2. Set Up Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your credentials
# Get these from your watsonx Orchestrate service instance
```

Your `.env` file should look like:

```env
ORCHESTRATE_API_KEY="your-ibm-cloud-api-key"
ORCHESTRATE_INSTANCE_ID="your-orchestrate-instance-id"
ORCHESTRATE_REGION="us-south"
ORCHESTRATE_AGENT_ID="optional-agent-id"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## ☁️ Deploy to IBM Cloud Code Engine

### Build and Push to IBM Cloud Container Registry

```bash
# Log in to IBM Cloud
ibmcloud login

# Target your resource group and region
ibmcloud target -g <resource-group> -r <region>

# Log in to Container Registry
ibmcloud cr login

# Build the image
docker build -t us.icr.io/<namespace>/orchestrate-chat:latest .

# Push the image
docker push us.icr.io/<namespace>/orchestrate-chat:latest
```

### Deploy in Code Engine

```bash
# Create a Code Engine project (if you don't have one)
ibmcloud ce project create --name orchestrate-chat

# Create the app
ibmcloud ce app create \
  --name orchestrate-chat \
  --image us.icr.io/<namespace>/orchestrate-chat:latest \
  --cpu 0.5 \
  --memory 1G \
  --min-scale 0 \
  --max-scale 1 \
  --env ORCHESTRATE_API_KEY="your-api-key" \
  --env ORCHESTRATE_INSTANCE_ID="your-instance-id" \
  --env ORCHESTRATE_REGION="us-south" \
  --env ORCHESTRATE_AGENT_ID="" \
  --wait
```

### Deploy via Console (Alternative)

1. Go to **IBM Cloud Code Engine** → **Projects** → **Start creating**
2. Click **Application**
3. Configure:
   - **Name**: `orchestrate-chat`
   - **Container image**: Use the image from Container Registry
   - **Port**: `8501`
   - **CPU/Memory**: 0.5 vCPU / 1 GB
   - **Min scale**: 0 (scales to zero when idle)
4. Under **Environment variables**, add your credentials
5. Click **Create**

Your app will be available at the provided URL.

---

## 🐳 Docker (Local)

```bash
# Build
docker build -t orchestrate-chat .

# Run
docker run -p 8501:8501 \
  -e ORCHESTRATE_API_KEY="your-api-key" \
  -e ORCHESTRATE_INSTANCE_ID="your-instance-id" \
  -e ORCHESTRATE_REGION="us-south" \
  -e ORCHESTRATE_AGENT_ID="" \
  orchestrate-chat
```

---

## 🔧 Configuration Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ORCHESTRATE_API_KEY` | ✅ Yes | — | Your IBM Cloud API key |
| `ORCHESTRATE_INSTANCE_ID` | ✅ Yes | — | Your watsonx Orchestrate instance GUID |
| `ORCHESTRATE_REGION` | ❌ No | `us-south` | API region (`us-south`, `eu-gb`, `eu-de`, `au-syd`, `jp-tok`) |
| `ORCHESTRATE_AGENT_ID` | ❌ No | — | Specific agent to use (blank = default) |

### Where to find your credentials

1. **Instance ID**: IBM Cloud → Resource List → watsonx Orchestrate → Copy the GUID from the service credentials or the browser URL
2. **API Key**: IBM Cloud → Manage → Access (IAM) → API Keys → Create
3. **Agent ID** (optional): In your Orchestrate instance, open the agent and copy its ID from the URL or details panel

---

## 📁 Project Structure

```
my-orchestrate-app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # Your credentials (gitignored)
├── .env.example           # Template for environment variables
├── Dockerfile             # Container definition
├── .gitignore             # Files to exclude from git
└── README.md              # This file
```

---

## 🤝 How It Works

1. The app authenticates with **IBM Cloud IAM** using your API key
2. It sends your messages to the **watsonx Orchestrate Chat API**
3. The Orchestrate agent processes the request (using any skills, integrations, or LLMs you've configured)
4. The response is displayed in a conversational Streamlit UI

---

## 📝 Notes

- The app does **not** store your credentials or conversation data — everything stays in memory
- Conversation context (`conversation_id`) is maintained within your browser session
- Reset the conversation anytime with the **New Conversation** button in the sidebar
- For production, use **IBM Cloud Secrets Manager** or Code Engine's built-in secrets instead of `.env`

---

## 📄 License

MIT
