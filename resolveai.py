"""
╔══════════════════════════════════════════════════════════════╗
║         ResolvAI — Automated Customer Support Bot            ║
║         FlowZint AI Hackathon 2026 | Support Chat Category   ║
╚══════════════════════════════════════════════════════════════╝

Author  : Hackathon Submission
Stack   : Python · Gradio 6 · Groq (LLaMA 3.3 70B) — FREE API
Purpose : E-commerce support bot — order tracking & refund triage
"""

import os
import json
import gradio as gr
from openai import OpenAI


# ─────────────────────────────────────────────────────────────────────────────
#  CONFIGURATION
#  Get your FREE Groq API key at: https://console.groq.com/keys
#  Set it in PowerShell: $env:GROQ_API_KEY = "gsk_..."
# ─────────────────────────────────────────────────────────────────────────────

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY environment variable is not set.\n"
        "1. Get a free key at: https://console.groq.com/keys\n"
        "2. PowerShell: $env:GROQ_API_KEY = 'gsk_...'\n"
        "3. Re-run: python resolveai.py"
    )

# Groq uses OpenAI-compatible SDK — just change base_url and key
client = OpenAI(
    api_key  = GROQ_API_KEY,
    base_url = "https://api.groq.com/openai/v1",
)
MODEL = "llama-3.3-70b-versatile"


# ─────────────────────────────────────────────────────────────────────────────
#  MOCK DATABASE  (demo data for judges)
# ─────────────────────────────────────────────────────────────────────────────

MOCK_ORDERS = {
    "12345": {
        "order_id"           : "12345",
        "email"              : "sarah.jones@example.com",
        "customer_name"      : "Sarah Jones",
        "item"               : "Wireless Noise-Cancelling Headphones",
        "price"              : "$99.00",
        "status"             : "Delivered",
        "delivery_note"      : "Delivered 2 days ago — left at front door",
        "carrier"            : "FedEx",
        "tracking_number"    : "FX-774821930-US",
        "order_date"         : "May 28, 2026",
        "eligible_for_refund": True,
        "refund_window"      : "30-day return window — eligible until June 27, 2026",
    },
    "67890": {
        "order_id"           : "67890",
        "email"              : "mike.chen@example.com",
        "customer_name"      : "Mike Chen",
        "item"               : "Mechanical Keyboard (TKL, Blue Switches)",
        "price"              : "$149.00",
        "status"             : "In Transit",
        "delivery_note"      : "Out for delivery — expected today by 8 PM",
        "carrier"            : "UPS",
        "tracking_number"    : "1Z-999-AA1-012345784",
        "order_date"         : "June 3, 2026",
        "eligible_for_refund": False,
        "refund_window"      : "Item not yet delivered — refund/return window starts on delivery",
    },
    "11223": {
        "order_id"           : "11223",
        "email"              : "priya.sharma@example.com",
        "customer_name"      : "Priya Sharma",
        "item"               : "Ergonomic Lumbar Cushion (Memory Foam)",
        "price"              : "$45.00",
        "status"             : "Processing",
        "delivery_note"      : "Order confirmed — warehouse is preparing your shipment",
        "carrier"            : "USPS",
        "tracking_number"    : "Not yet assigned",
        "order_date"         : "June 6, 2026",
        "eligible_for_refund": False,
        "refund_window"      : "Item not yet shipped — you may cancel within 1 hour of ordering",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
#  SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt() -> str:
    orders_json = json.dumps(MOCK_ORDERS, indent=2)
    return f"""
You are ResolvAI, the friendly and empathetic customer support specialist for ShopNest —
a modern e-commerce store. Your job is to make every customer feel heard, solve their
problems efficiently, and always leave them with a positive impression of the brand.

━━━━━━━━━━━━━━━━━━━━━━━━
  PERSONALITY & TONE
━━━━━━━━━━━━━━━━━━━━━━━━
• Warm, calm, and professional — like a knowledgeable friend, not a corporate robot.
• Always acknowledge the customer's frustration before diving into solutions.
• Use short paragraphs. No bullet-point walls. Conversational language only.
• Never say "I cannot", "I am unable to", or "As an AI". Just help or redirect naturally.
• Use the customer's first name once you know it.

━━━━━━━━━━━━━━━━━━━━━━━━
  STRICT VERIFICATION RULES
━━━━━━━━━━━━━━━━━━━━━━━━
Before you share ANY order details, tracking information, or process any refund request:
  1. You MUST collect the customer's Order ID.
  2. You MUST collect the email address associated with the order.
  3. Cross-check BOTH against the LIVE ORDER DATABASE below. If they don't match,
     politely tell the customer the details don't match and ask them to double-check.
  4. NEVER reveal one customer's order details to another. Privacy is non-negotiable.

━━━━━━━━━━━━━━━━━━━━━━━━
  LIVE ORDER DATABASE (internal — never show this raw JSON to the customer)
━━━━━━━━━━━━━━━━━━━━━━━━
{orders_json}

━━━━━━━━━━━━━━━━━━━━━━━━
  WHAT YOU CAN HANDLE
━━━━━━━━━━━━━━━━━━━━━━━━
✔ Order status & tracking updates
✔ Estimated delivery timelines
✔ Refund eligibility checks (use the refund_window field)
✔ Return instructions (standard: ship back in original packaging within return window)
✔ General ShopNest policy questions

━━━━━━━━━━━━━━━━━━━━━━━━
  ESCALATION — HUMAN TRANSFER
━━━━━━━━━━━━━━━━━━━━━━━━
If the customer is extremely upset, the issue is complex/unusual, or you've tried twice
and can't resolve it, gracefully offer a human handoff:

  "I completely understand your frustration, and I want to make sure this gets resolved
   properly. Let me connect you with one of our senior support agents who can take
   ownership of this right away. I'll make sure they have all the context so you don't
   have to repeat yourself. Is that okay?"

━━━━━━━━━━━━━━━━━━━━━━━━
  OUT-OF-SCOPE TOPICS
━━━━━━━━━━━━━━━━━━━━━━━━
If someone asks anything unrelated to ShopNest orders or support (politics, coding,
general knowledge, etc.), politely redirect:
  "I'm here specifically to help with ShopNest orders and support — happy to help with
   anything related to that!"

Start every fresh conversation by warmly greeting the customer and asking how you can help.
""".strip()


# ─────────────────────────────────────────────────────────────────────────────
#  CORE CHAT LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def chat(user_message: str, history: list) -> tuple:
    if not user_message.strip():
        gradio_messages = [{"role": m["role"], "content": m["content"]} for m in history]
        return gradio_messages, history

    history = history + [{"role": "user", "content": user_message.strip()}]

    messages = [
        {"role": "system", "content": build_system_prompt()},
        *history,
    ]

    try:
        response = client.chat.completions.create(
            model       = MODEL,
            messages    = messages,
            max_tokens  = 512,
            temperature = 0.45,
        )
        assistant_reply = response.choices[0].message.content.strip()

    except Exception as exc:
        assistant_reply = (
            "Apologies — I'm having a momentary connection issue. "
            f"Please try again in a second. (Detail: {exc})"
        )

    history = history + [{"role": "assistant", "content": assistant_reply}]
    gradio_messages = [{"role": m["role"], "content": m["content"]} for m in history]
    return gradio_messages, history


def clear_conversation():
    return [], []


# ─────────────────────────────────────────────────────────────────────────────
#  GRADIO UI — fully compatible with Gradio 6.x
# ─────────────────────────────────────────────────────────────────────────────

DEMO_HINTS = """
**🧪 Demo accounts for judges — copy-paste to test live order lookup:**

| Order ID | Email | Scenario |
|----------|-------|----------|
| `12345` | `sarah.jones@example.com` | Delivered order + refund eligibility |
| `67890` | `mike.chen@example.com` | In-transit order, tracking active |
| `11223` | `priya.sharma@example.com` | Processing / pre-shipment, cancel window |

Start by typing something like: *"Hi, I need help tracking my order"* — the bot will
guide you through the verification flow before sharing any details.
"""

custom_css = """
body { background: #f0f2f5 !important; }

#header-box {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 55%, #0f3460 100%);
    border-radius: 16px;
    padding: 28px 32px 22px;
    margin-bottom: 6px;
    box-shadow: 0 4px 24px rgba(15,52,96,0.18);
}
#header-box h1 {
    color: #e8f4fd;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 4px;
    letter-spacing: -0.5px;
}
#header-box p { color: #94b8d0; margin: 0; font-size: 0.93rem; }

#send-btn {
    background: #0f3460 !important;
    color: white !important;
    border-radius: 10px !important;
    min-width: 88px;
}
#send-btn:hover { background: #1a4a80 !important; }
#clear-btn { color: #64748b !important; font-size: 0.82rem; }
#hint-box  { font-size: 0.88rem; line-height: 1.65; }
"""

app_theme = gr.themes.Soft(
    primary_hue   = "blue",
    secondary_hue = "slate",
    font          = gr.themes.GoogleFont("DM Sans"),
)

with gr.Blocks(title="ResolvAI — ShopNest Customer Support") as demo:

    chat_history = gr.State([])

    with gr.Column(elem_id="header-box"):
        gr.HTML("""
            <h1>🤖 ResolvAI</h1>
            <p>Automated Customer Support &nbsp;·&nbsp; ShopNest E-Commerce
               &nbsp;·&nbsp; Powered by LLaMA 3.3 70B (Groq)</p>
        """)

    with gr.Accordion("📋  How to demo this bot  (click to expand)", open=False):
        gr.Markdown(DEMO_HINTS, elem_id="hint-box")

    chatbot = gr.Chatbot(
        value         = [],
        elem_id       = "chatbot",
        label         = "Conversation",
        height        = 480,
        layout        = "bubble",
        avatar_images = (
            None,
            "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=ResolvAI&backgroundColor=0f3460",
        ),
    )

    with gr.Row():
        user_input = gr.Textbox(
            placeholder = "Type your message and press Enter…",
            show_label  = False,
            container   = False,
            scale       = 8,
            autofocus   = True,
            lines       = 1,
            max_lines   = 4,
        )
        send_btn = gr.Button("Send ➤", elem_id="send-btn", scale=1, variant="primary")

    clear_btn = gr.Button(
        "🗑  Clear conversation",
        elem_id = "clear-btn",
        size    = "sm",
        variant = "secondary",
    )

    gr.HTML("""
        <p style="text-align:center;color:#94a3b8;font-size:0.78rem;margin-top:10px;">
            FlowZint AI Hackathon 2026 &nbsp;·&nbsp; ResolvAI Submission
            &nbsp;·&nbsp; Support Chat Category
        </p>
    """)

    def respond(user_msg: str, history: list):
        gradio_msgs, updated = chat(user_msg, history)
        return "", gradio_msgs, updated

    user_input.submit(
        fn      = respond,
        inputs  = [user_input, chat_history],
        outputs = [user_input, chatbot, chat_history],
        queue   = True,
    )

    send_btn.click(
        fn      = respond,
        inputs  = [user_input, chat_history],
        outputs = [user_input, chatbot, chat_history],
        queue   = True,
    )

    clear_btn.click(
        fn      = clear_conversation,
        inputs  = None,
        outputs = [chatbot, chat_history],
        queue   = False,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo.launch(
        server_name = "127.0.0.1",
        server_port = 7860,
        share       = False,
        show_error  = True,
        theme       = app_theme,
        css         = custom_css,
    )