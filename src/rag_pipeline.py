"""
Think of this like a film director.
The director doesn't act, design sets, or write music —
they coordinate everyone who does. They call each department
in the right order and make sure the output of one feeds
correctly into the next.

This file calls query_planner, retrieval_agent, and synthesizer
in sequence. It's the only file app.py needs to talk to.
"""

from src.vector_store    import VectorStore
from src.query_planner   import decompose_question
from src.retrieval_agent import retrieve_all
from src.synthesizer     import synthesize_answer


class AgenticRAGPipeline:
    def __init__(self, pdf_dir: str = "data"):
        print("[Pipeline] Initializing vector store...")
        self.store = VectorStore()
        self.store.build_from_pdfs(pdf_dir)
        print(f"[Pipeline] Ready. {self.store.collection.count()} chunks loaded.")

    def ask(self, question: str) -> dict:
        print(f"\n{'='*60}")
        print(f"[Pipeline] Question: {question}")
        print(f"{'='*60}")

        # Step 1: decompose
        print("\n[Pipeline] Step 1: Decomposing question...")
        sub_queries = decompose_question(question)
        print(f"[Pipeline] Sub-queries: {sub_queries}")

        # Step 2: retrieve with agentic loop
        print("\n[Pipeline] Step 2: Retrieving evidence...")
        outcomes = retrieve_all(sub_queries, self.store)

        # Step 3: synthesize
        print("\n[Pipeline] Step 3: Synthesizing answer...")
        result = synthesize_answer(question, outcomes)

        result["question"]    = question
        result["sub_queries"] = sub_queries

        print(f"\n[Pipeline] Done. Retrieval quality: {result['retrieval_quality']}/10")
        return result
