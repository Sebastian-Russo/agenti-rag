"""
Think of this like a librarian who has read every Harry Potter book,
cut the text into 500-character index cards, and filed them two ways:
  1. By meaning   (semantic/embedding search — ChromaDB)
  2. By exact words (keyword search — BM25)

When you ask a question, she checks both filing systems and returns
the best cards from both, deduplicated.
"""

import os
import glob
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from rank_bm25 import BM25Okapi

from src.config import (
    EMBEDDING_MODEL, VECTORSTORE_PATH, COLLECTION_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_PER_SUBQUERY
)


def _extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _chunk_text(text: str) -> list[str]:
    # Overlap means a sentence at a boundary appears in TWO chunks,
    # so retrieval never misses it because it got split awkwardly.
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + CHUNK_SIZE])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


class VectorStore:
    def __init__(self):
        self.embedder   = SentenceTransformer(EMBEDDING_MODEL)
        self.client     = chromadb.PersistentClient(path=VECTORSTORE_PATH)
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)
        self._bm25       = None
        self._all_chunks = None

    def build_from_pdfs(self, pdf_dir: str = "data") -> None:
        if self.collection.count() > 0:
            print(f"Vector store already has {self.collection.count()} chunks. Skipping build.")
            return

        pdf_paths = glob.glob(os.path.join(pdf_dir, "*.pdf"))
        if not pdf_paths:
            raise FileNotFoundError(f"No PDFs found in '{pdf_dir}/'")

        all_chunks, all_ids = [], []
        for pdf_path in sorted(pdf_paths):
            print(f"Processing {os.path.basename(pdf_path)} ...")
            text      = _extract_text_from_pdf(pdf_path)
            chunks    = _chunk_text(text)
            book_name = os.path.splitext(os.path.basename(pdf_path))[0]
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_ids.append(f"{book_name}_chunk_{i}")

        print(f"Embedding {len(all_chunks)} chunks ...")
        embeddings = self.embedder.encode(all_chunks, show_progress_bar=True).tolist()
        self.collection.add(documents=all_chunks, embeddings=embeddings, ids=all_ids)
        print(f"Stored {len(all_chunks)} chunks.")

    def _ensure_bm25(self) -> None:
        if self._bm25 is not None:
            return
        result           = self.collection.get()
        self._all_chunks = result["documents"]
        self._bm25       = BM25Okapi([doc.lower().split() for doc in self._all_chunks])

    def query(self, query_text: str, top_k: int = TOP_K_PER_SUBQUERY) -> list[dict]:
        self._ensure_bm25()

        # Semantic search — finds by meaning
        query_embedding = self.embedder.encode(query_text).tolist()
        sem_result      = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        sem_chunks      = sem_result["documents"][0]
        sem_ids         = sem_result["ids"][0]

        # Keyword search — finds by exact words
        scores      = self._bm25.get_scores(query_text.lower().split())
        top_idx     = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        stored      = self.collection.get()
        bm25_chunks = [stored["documents"][i] for i in top_idx]
        bm25_ids    = [stored["ids"][i]       for i in top_idx]

        # Merge and deduplicate
        seen, results = set(), []
        for text, doc_id in zip(sem_chunks + bm25_chunks, sem_ids + bm25_ids):
            if doc_id not in seen:
                seen.add(doc_id)
                results.append({"id": doc_id, "text": text})
        return results[:top_k]
