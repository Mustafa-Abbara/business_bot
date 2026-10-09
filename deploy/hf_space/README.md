---
title: Milo, EchoNest's Memory Concierge
emoji: 🪺
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 6.29.1
python_version: "3.12"
app_file: app.py
pinned: false
short_description: Agent-powered business assistant (EECE 503P/798S)
---

# Milo, EchoNest's Memory Concierge

An agent-powered business assistant for **EchoNest**, a fictional digital-memory studio. It was built for EECE
503P/798S (Agentic Systems), Assignment C3.

Milo answers questions from the business documents, routes each message (general / lead / feedback), collects
leads with `record_customer_interest`, logs unanswered questions and feedback with `record_feedback`, and checks his
own replies before sending them. The LLM is Gemini (free tier), called through the `openai` SDK.

**Try:**
- "What does EchoNest actually create?"
- "I'd like a Life Timeline for my grandmother."
- "Can you restore damaged film negatives?"

**Notes:**
- Leads and feedback are written to JSONL files inside the Space. They are **lost when the Space restarts**: this is a
  demo, not a CRM.
- The Space runs on a free-tier API key (about 500 requests per day, 3–4 per message). When the quota is used up,
  Milo says so politely.

Source code, tests and documentation: https://github.com/Mustafa-Abbara/business_bot
