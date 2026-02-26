"""
Think of this like a researcher at a library who has been given a specific
sub-question to answer. They search the shelves, bring back some books,
and check: "Does this actually answer my question?"

If yes — done. If no — they don't give up. They think about why the
search failed, try a different search term, and go back to the shelves.
They only stop when they're satisfied OR they've hit their retry limit.

This is the agentic loop. Everything else supports this file.
"""

from src.vector_store import VectorStore
from src.evaluator    import evaluate_chunks, EvaluationResult
from src.config       import TOP_K_PER_SUBQUERY, MAX_RETRIEVAL_ATTEMPTS


class AttemptLog:
    """A record of one search attempt — what was searched and what came back."""
    def __init__(self, query_used: str, chunks: list[dict], evaluation: EvaluationResult):
        self.query_used  = query_used
        self.chunks      = chunks
        self.evaluation  = evaluation


class RetrievalOutcome:
    """Everything that happened when retrieving chunks for one sub-query."""
    def __init__(self, sub_query: str):
        self.sub_query    = sub_query
        self.final_chunks = []      # the chunks we're actually using
        self.attempts     = []      # full log of every search attempt
        self.final_score  = 0
        self.succeeded    = False   # True if we hit the relevance threshold


def retrieve_for_subquery(sub_query: str, store: VectorStore) -> RetrievalOutcome:
    outcome       = RetrievalOutcome(sub_query)
    current_query = sub_query   # may be reformulated on retry

    for attempt_num in range(MAX_RETRIEVAL_ATTEMPTS):
        print(f"  [RetrievalAgent] Attempt {attempt_num + 1}/{MAX_RETRIEVAL_ATTEMPTS}: '{current_query}'")

        # Step 1: search
        chunks = store.query(current_query, top_k=TOP_K_PER_SUBQUERY)

        # Step 2: evaluate
        # Note: always evaluate against the ORIGINAL sub_query —
        # the goal hasn't changed, only the search strategy has.
        evaluation = evaluate_chunks(sub_query, chunks)
        outcome.attempts.append(AttemptLog(current_query, chunks, evaluation))

        print(f"  [RetrievalAgent] Score: {evaluation.score}/10 — {evaluation.reason}")

        # Step 3: decide
        if evaluation.is_sufficient:
            outcome.final_chunks = chunks
            outcome.final_score  = evaluation.score
            outcome.succeeded    = True
            print(f"  [RetrievalAgent] ✓ Accepted.")
            return outcome

        # Not sufficient — retry if we have attempts left and a new query
        if attempt_num < MAX_RETRIEVAL_ATTEMPTS - 1 and evaluation.reformulated_query:
            print(f"  [RetrievalAgent] ✗ Reformulating to: '{evaluation.reformulated_query}'")
            current_query = evaluation.reformulated_query
        else:
            # Out of retries — use the best attempt we logged
            best = max(outcome.attempts, key=lambda a: a.evaluation.score)
            outcome.final_chunks = best.chunks
            outcome.final_score  = best.evaluation.score
            outcome.succeeded    = False
            print(f"  [RetrievalAgent] Max attempts reached. Using best (score: {outcome.final_score}).")
            return outcome

    return outcome


def retrieve_all(sub_queries: list[str], store: VectorStore) -> list[RetrievalOutcome]:
    """Run the retrieval loop for every sub-query. Called by the pipeline."""
    outcomes = []
    for i, sub_query in enumerate(sub_queries):
        print(f"\n[RetrievalAgent] Sub-query {i+1}/{len(sub_queries)}: '{sub_query}'")
        outcomes.append(retrieve_for_subquery(sub_query, store))
    return outcomes