"""
Think of this like a detective briefing before an investigation.
A good detective doesn't just run off with the original tip —
they break it down first: "Who are the suspects? What's the timeline?
What's the motive?" Each angle gets its own investigation.

This file does the same for questions. A complex question gets broken
into focused sub-queries, each targeted enough for a clean vector search.
"""

import json
import anthropic
from src.config import ANTHROPIC_API_KEY, CLAUDE_MODEL_FAST, MAX_SUBQUERIES


def decompose_question(question: str) -> list[str]:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""You are a query planning assistant for a Harry Potter book search system.

User question: "{question}"

Break this into {MAX_SUBQUERIES} or fewer focused sub-queries for separate searches.

Rules:
- Each sub-query should be specific and self-contained
- Cover different aspects of the original question
- Phrase as search queries, not questions (e.g. "Snape loyalty Dumbledore" not "Was Snape loyal?")
- If the question is already simple and focused, return just 1 sub-query

Respond with ONLY a JSON array of strings. No explanation, no markdown.
Example: ["sub-query one", "sub-query two"]"""

    response = client.messages.create(
        model      = CLAUDE_MODEL_FAST,
        max_tokens = 300,
        messages   = [{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    try:
        sub_queries = json.loads(raw)
        if not isinstance(sub_queries, list):
            raise ValueError("Expected a list")
        return [str(q) for q in sub_queries[:MAX_SUBQUERIES]]
    except (json.JSONDecodeError, ValueError):
        # If parsing fails, fall back to the original question as-is
        print(f"[QueryPlanner] JSON parse failed, using original question. Raw: {raw}")
        return [question]
