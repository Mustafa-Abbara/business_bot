# business_bot — Agent-Powered Business Assistant

EECE 503P/798S (Agentic Systems), Assignment C3.

A chatbot that represents a fictional business: it answers questions from the business documents, routes each
message (general / lead / feedback), collects leads, and logs unanswered questions and feedback through tool calls.
It runs on Gemini through the `openai` SDK (OpenAI-compatible endpoint) and is served with a Gradio ChatInterface.

> 🚧 Work in progress — Stage 0 (environment and repo skeleton) is complete.

## Project structure

```
business_bot/
  me/                    # about_business.pdf + business_summary.txt (Stage 1)
  logs/                  # runtime JSONL logs (git-ignored)
  tests/                 # unit tests and router cases
  business_agent.ipynb   # main notebook
  .env.example           # copy to .env and add your key
  .gitignore
  README.md
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install openai python-dotenv pypdf gradio ipykernel
copy .env.example .env          # macOS/Linux: cp .env.example .env
```

Then put your Gemini key (from Google AI Studio) in `.env` as `GEMINI_API_KEY=...` — no quotes, no spaces.
In Colab, add `GEMINI_API_KEY` under **Secrets** instead and enable notebook access.

Open `business_agent.ipynb` and select the **Python (business_bot)** kernel.

## Library notes

The assignment mentions `google.generativeai` and `openai.ChatCompletion`. The first has been deprecated since
November 30, 2025, and the second was removed in `openai` 1.0. This project uses their supported replacements:
`client.chat.completions.create(...)` from the current `openai` SDK, pointed at Gemini's OpenAI-compatible endpoint.
