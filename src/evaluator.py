"""
Think of this like a quality control inspector on an assembly line.
After each search, the inspector checks the retrieved chunks and asks:
"Is this good enough to ship, or do we need to redo this part?"

If the parts are bad, the inspector doesn't just reject them —
they suggest exactly what to fix so the next attempt is better.

Again Haiku — scoring and reformulating is simple structured reasoning.
Notice EvaluationResult is just a data container, it holds the outcome so the next file can act on it.
"""

import json
import anthropic
from src.config import ANTHROPIC_API_KEY, CLAUDE_MODEL_FAST, RELEVANCE_THRESHOLD


class EvaluationResult:
    def __init__(self, score: int, is_sufficient: bool, reason: str, reformulated_query: str | None):
        self.score              = score
        self.is_sufficient      = is_sufficient       # True = accept, False = re-search
        self.reason             = reason
        self.reformulated_query = reformulated_query  # only set when is_sufficient=False


def evaluate_chunks(sub_query: str, chunks: list[dict]) -> EvaluationResult:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    chunk_text = "\n\n---\n\n".join(
        f"Chunk {i+1}:\n{chunk['text']}" for i, chunk in enumerate(chunks)
    )

    prompt = f"""You are evaluating search results for a Harry Potter Q&A system.

Sub-query: "{sub_query}"

Retrieved passages:
{chunk_text}

Do these passages contain sufficient information to answer the sub-query?

Respond with ONLY a JSON object in this exact format:
{{
  "score": <integer 0-10>,
  "reason": "<one sentence explaining the score>",
  "reformulated_query": "<alternative search query if score < {RELEVANCE_THRESHOLD}, otherwise null>"
}}

Scoring guide:
  8-10: Passages directly and fully address the sub-query
  6-7:  Passages address the sub-query but miss some details
  4-5:  Tangentially related but missing key information
  0-3:  Passages do not address the sub-query at all

If score < {RELEVANCE_THRESHOLD}, provide a reformulated_query using different
keywords or a different angle. If score >= {RELEVANCE_THRESHOLD}, set it to null."""

    response = client.messages.create(
        model      = CLAUDE_MODEL_FAST,
        max_tokens = 200,
        messages   = [{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    try:
        data  = json.loads(raw)
        score = int(data.get("score", 0))
        return EvaluationResult(
            score              = score,
            is_sufficient      = score >= RELEVANCE_THRESHOLD,
            reason             = data.get("reason", ""),
            reformulated_query = data.get("reformulated_query")
        )
    except (json.JSONDecodeError, ValueError, KeyError):
        # If parsing fails, conservatively accept what we have
        print(f"[Evaluator] JSON parse failed, accepting chunks. Raw: {raw}")
        return EvaluationResult(
            score              = RELEVANCE_THRESHOLD,
            is_sufficient      = True,
            reason             = "Evaluation parse error — accepting chunks",
            reformulated_query = None
        )
