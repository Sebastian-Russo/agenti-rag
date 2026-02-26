"""
Think of this like a lawyer giving a closing argument.
By this point, all the evidence has been gathered from multiple angles.
The lawyer's job isn't to find more evidence — it's to take everything
on the table and weave it into one coherent, convincing narrative.

This file does the same. It takes chunks from every sub-query,
labeled by which angle they came from, and writes the final answer.
"""

import anthropic
from src.config          import ANTHROPIC_API_KEY, CLAUDE_MODEL_SMART
from src.retrieval_agent import RetrievalOutcome


def synthesize_answer(original_question: str, outcomes: list[RetrievalOutcome]) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Build a labeled evidence block so Claude knows which chunks
    # answered which angle of the question
    evidence_sections = []
    for outcome in outcomes:
        chunks_text = "\n\n".join(
            f"  Passage {j+1}: {chunk['text']}"
            for j, chunk in enumerate(outcome.final_chunks)
        )
        quality_note = f"(retrieval score: {outcome.final_score}/10)"
        evidence_sections.append(
            f'Evidence for: "{outcome.sub_query}" {quality_note}\n{chunks_text}'
        )

    all_evidence = ("\n\n" + "=" * 60 + "\n\n").join(evidence_sections)

    prompt = f"""You are answering a question about the Harry Potter book series.
You have retrieved passages from the books, organized by the specific aspect
of the question they address.

ORIGINAL QUESTION:
{original_question}

RETRIEVED EVIDENCE:
{all_evidence}

Instructions:
- Answer the original question using ONLY the provided evidence
- Structure your answer to address all aspects of the question
- If evidence for some aspects is weak, acknowledge this naturally
- Do not invent anything not supported by the passages
- Write in clear paragraphs, not bullet points"""

    response = client.messages.create(
        model      = CLAUDE_MODEL_SMART,
        max_tokens = 1000,
        messages   = [{"role": "user", "content": prompt}]
    )

    avg_score = sum(o.final_score for o in outcomes) / len(outcomes) if outcomes else 0

    return {
        "answer":              response.content[0].text.strip(),
        "sub_query_summaries": [
            {
                "sub_query":   o.sub_query,
                "score":       o.final_score,
                "succeeded":   o.succeeded,
                "attempts":    len(o.attempts),
                "chunks_used": len(o.final_chunks)
            }
            for o in outcomes
        ],
        "retrieval_quality":  round(avg_score, 1),
        "total_chunks_used":  sum(len(o.final_chunks) for o in outcomes)
    }
