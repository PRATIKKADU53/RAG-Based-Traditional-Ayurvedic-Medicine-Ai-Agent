import streamlit as st
import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

# ------------------- CONFIGURATION -------------------
API_KEY = os.getenv("ORCHESTRATE_API_KEY")
INSTANCE_ID = os.getenv("ORCHESTRATE_INSTANCE_ID")
REGION = os.getenv("ORCHESTRATE_REGION", "us-south")
AGENT_ID = os.getenv("ORCHESTRATE_AGENT_ID")

# Validate required config
missing_vars = []
if not API_KEY:
    missing_vars.append("ORCHESTRATE_API_KEY")
if not INSTANCE_ID:
    missing_vars.append("ORCHESTRATE_INSTANCE_ID")
if not AGENT_ID:
    missing_vars.append("ORCHESTRATE_AGENT_ID")
if missing_vars:
    st.error(f"Missing required environment variables: {', '.join(missing_vars)}. Please check your .env file.")
    st.stop()

# ------------------- IAM TOKEN (with caching) -------------------
_token_cache = {"token": None, "expires_at": 0}

def get_iam_token(api_key):
    """Get (and cache) IBM Cloud IAM access token"""
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["token"]

    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    result = response.json()
    _token_cache["token"] = result["access_token"]
    _token_cache["expires_at"] = now + result.get("expires_in", 3600)
    return result["access_token"]


# ------------------- ORCHESTRATE API -------------------
def _api_base():
    return f"https://api.{REGION}.watson-orchestrate.cloud.ibm.com/instances/{INSTANCE_ID}"


def _auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def call_orchestrate_agent(user_input, thread_id=None):
    """Send message to watsonx Orchestrate agent and get response.

    Uses the Runs API (async) with polling for the result.
    Returns (response_text, thread_id).
    """
    try:
        token = get_iam_token(API_KEY)
        base = _api_base()
        headers = _auth_headers(token)

        # 1. Start a run
        payload = {
            "message": {"role": "user", "content": user_input},
            "agent_id": AGENT_ID,
        }
        if thread_id:
            payload["thread_id"] = thread_id

        run_resp = requests.post(
            f"{base}/v1/orchestrate/runs?stream=false",
            json=payload,
            headers=headers,
            timeout=30,
        )
        run_resp.raise_for_status()
        run_data = run_resp.json()

        new_thread_id = run_data.get("thread_id") or thread_id
        if not new_thread_id:
            return "Error: No thread_id returned from API.", None

        # 2. Poll for messages
        for attempt in range(15):
            time.sleep(1.5)
            msgs_resp = requests.get(
                f"{base}/v1/orchestrate/threads/{new_thread_id}/messages",
                headers=headers,
                timeout=15,
            )
            if msgs_resp.status_code != 200:
                continue

            messages = msgs_resp.json()
            if not isinstance(messages, list):
                continue

            # Find the latest assistant message
            assistant_msgs = [m for m in messages if m.get("role") == "assistant"]
            if assistant_msgs:
                latest = assistant_msgs[-1]
                # Extract text content
                content = latest.get("content", "")
                if isinstance(content, list):
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict):
                            text_parts.append(block.get("text", "") or block.get("content", "") or "")
                    return "\n".join(text_parts), new_thread_id
                elif isinstance(content, str) and content.strip():
                    return content, new_thread_id

        return "The agent took too long to respond. Please try again.", new_thread_id

    except requests.exceptions.RequestException as e:
        detail = ""
        if hasattr(e, "response") and e.response is not None:
            try:
                detail = e.response.json()
            except Exception:
                detail = e.response.text[:500]
        return f"**API Error**: {str(e)}", None
    except Exception as e:
        return f"**Error**: {str(e)}", None


# ------------------- STREAMLIT UI -------------------
st.set_page_config(
    page_title="Ayurvedic Medicine AI — Grandma Anong's Remedies",
    page_icon="🌿",
    layout="centered",
)

st.title("🌿 Ayurvedic Medicine AI")
st.caption("Powered by Grandma Anong's 5-generation traditional knowledge + IBM watsonx Orchestrate")

# Sidebar
with st.sidebar:
    st.header("🌿 About This Assistant")
    st.markdown(
        "This AI is powered by **Grandma Anong's** proprietary Ayurvedic knowledge — "
        "authentic herbal remedies and traditional healing practices passed down "
        "through **five generations** in Kerala, India."
    )
    st.markdown(
        "Ask about remedies for common health concerns using everyday "
        "kitchen ingredients like ginger, turmeric, tulsi, amla, neem, "
        "honey, cumin, and lemon."
    )
    st.divider()
    st.markdown("**🔹 What it can do:**")
    st.markdown("- Suggest Ayurvedic home remedies")
    st.markdown("- Provide step-by-step preparation")
    st.markdown("- Adjust ingredient quantities")
    st.markdown("- Explain traditional uses")
    st.markdown(f"**Region:** {REGION}")
    st.markdown(f"**Agent:** `{AGENT_ID[:8]}...`")

    st.divider()

    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = None
        st.rerun()

    st.divider()
    st.markdown("**🌱 Common Remedies**")
    if st.button("🤧 Cold & Cough", use_container_width=True):
        st.session_state.quick_prompt = "I have a cold and cough. Can you suggest an Ayurvedic remedy?"
    if st.button("🤢 Indigestion", use_container_width=True):
        st.session_state.quick_prompt = "I have indigestion. What Ayurvedic remedy would help?"
    if st.button("🤕 Headache", use_container_width=True):
        st.session_state.quick_prompt = "Do you have an Ayurvedic remedy for headaches?"
    if st.button("🩹 Skin issue", use_container_width=True):
        st.session_state.quick_prompt = "Can you suggest an Ayurvedic remedy for a skin irritation?"

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Handle quick prompt
if st.session_state.quick_prompt:
    prompt_text = st.session_state.quick_prompt
    st.session_state.quick_prompt = None
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    st.chat_message("user").markdown(prompt_text)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply, tid = call_orchestrate_agent(prompt_text, st.session_state.thread_id)
            if tid:
                st.session_state.thread_id = tid
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply, tid = call_orchestrate_agent(prompt, st.session_state.thread_id)
            if tid:
                st.session_state.thread_id = tid
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

st.divider()
st.caption("Built with Streamlit + IBM watsonx Orchestrate")
