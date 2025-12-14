import os

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# Prefer environment variable (best for Streamlit Cloud / instructor machines)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Optional local fallback for the assignment template (secrets.py or my_secrets.py)
if not OPENAI_API_KEY:
    try:
        from my_secrets import OPENAI_API_KEY as _K  # optional file
        OPENAI_API_KEY = _K
    except Exception:
        OPENAI_API_KEY = None


def _get_client():
    if OpenAI is None:
        return None, "OpenAI package is not installed. Run: pip install -r requirements.txt"
    if not OPENAI_API_KEY:
        return None, (
            "Missing OPENAI_API_KEY. Set it as an environment variable "
            "or define it in my_secrets.py"
        )
    return OpenAI(api_key=OPENAI_API_KEY), None


# -------------------------
# 1) REQUIRED LLM FEATURE
# -------------------------
def summarize_text(text: str) -> str:
    """Summarize text in 2–4 simple sentences (assignment requirement)."""
    if not text.strip():
        return "Please enter some text to summarize."

    client, err = _get_client()
    if err:
        return err

    prompt = f"Summarize the following in 2–4 simple sentences:\n\n{text}"

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=300,
    )
    return response.output_text


# -------------------------
# 2) BONUS: TASK-FOCUSED CHATBOT UI
# -------------------------
TUTOR_SYSTEM_PROMPT = (
    "You are a friendly programming tutor for first-year university students.\n"
    "Your job is to help the user complete tasks related to:\n"
    "1) Basic Python (variables, loops, functions, errors)\n"
    "2) Basic SQL and SQLite queries\n"
    "3) Understanding this Streamlit project (login, SQLite, summarizer, chatbot)\n\n"
    "Rules:\n"
    "- Keep answers short and clear (3–8 sentences).\n"
    "- If the user asks for steps, give numbered steps.\n"
    "- If the user pastes code, explain what it does and point out obvious mistakes.\n"
    "- If something is missing (like API key), explain how to fix it simply.\n"
)


def chatbot_reply(chat_history):
    """
    Task-focused chatbot that uses a non-trivial system prompt.
    chat_history is a list of dicts like:
    [{"role": "user"|"assistant", "content": "..."}]
    """
    client, err = _get_client()
    if err:
        return err

    # Convert structured history into a clean transcript
    history_lines = []
    for msg in chat_history:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if not content:
            continue
        label = "User" if role == "user" else "Tutor"
        history_lines.append(f"{label}: {content}")

    history_text = "\n".join(history_lines).strip()

    prompt = (
        f"{TUTOR_SYSTEM_PROMPT}\n"
        f"Conversation so far:\n{history_text}\n\n"
        f"Tutor:"
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=400,
    )
    return response.output_text
