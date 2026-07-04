# 🤖 ResolvAI — Automated Customer Support Bot

> FlowZint AI Hackathon 2026 · Support Chat Category

An AI-powered customer support chatbot for **ShopNest** e-commerce, built with Python, Gradio 6, and the **Groq free API (LLaMA 3.3 70B)**. ResolvAI handles order tracking, refund triage, and customer queries with a warm, conversational tone — and enforces strict identity verification before sharing any order data.

---

## ✨ Features

- 🔐 **Two-factor verification** — Order ID + email must match before any data is shared
- 📦 **Order tracking** — Real-time status, carrier, tracking number, and delivery ETA
- 💸 **Refund triage** — Checks return window eligibility and guides customers through returns
- 🙋 **Human escalation** — Detects frustration and offers a warm handoff with full context
- 🚫 **Scope enforcement** — Redirects off-topic queries to keep the bot focused
- 💬 **Empathetic tone** — Warm and conversational, never robotic

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.x |
| UI Framework | Gradio 6 |
| LLM | LLaMA 3.3 70B via Groq |
| API SDK | OpenAI-compatible (groq endpoint) |
| Data | JSON mock order database |

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/kavinraj292008-a11y/resolveai-chatbot.git
cd resolveai-chatbot
```

### 2. Install dependencies
```bash
pip install gradio openai
```

### 3. Get a free Groq API key
Sign up at **https://console.groq.com/keys** — completely free, no credit card needed.

### 4. Set your API key

**Windows PowerShell:**
```powershell
$env:GROQ_API_KEY = "gsk_..."
```

**Linux / macOS:**
```bash
export GROQ_API_KEY="gsk_..."
```

### 5. Run the app
```bash
python resolveai.py
```

Then open **http://localhost:7860** in your browser.

---

## 🧪 Demo Accounts

Use these to test the live order lookup flow:

| Order ID | Email | Scenario |
|----------|-------|----------|
| `12345` | `sarah.jones@example.com` | Delivered order + refund eligible |
| `67890` | `mike.chen@example.com` | In-transit, tracking active |
| `11223` | `priya.sharma@example.com` | Processing, cancel window open |

Start with: *"Hi, I need help tracking my order"*

---

## 🔒 Security Notes

- API key is loaded from environment variables only — never hardcoded
- `.env` and `.venv/` are excluded via `.gitignore`
- Identity verification prevents cross-customer data leakage

---

## 📁 Project Structure

```
resolveai-chatbot/
├── resolveai.py      # Main application
├── README.md         # This file
└── .gitignore        # Excludes venv, secrets, cache
```

---

<p align="center">
  Built for FlowZint AI Hackathon 2026 &nbsp;·&nbsp; Support Chat Category
</p>