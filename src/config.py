import os
from dotenv import load_dotenv

load_dotenv()

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Use a lightweight model for planning and evaluation (fast, cheap)
CLAUDE_MODEL_FAST  = "claude-haiku-4-5-20251001"

# Use a stronger model for the final answer (quality matters here)
CLAUDE_MODEL_SMART = "claude-sonnet-4-6"

# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Vector Store
VECTORSTORE_PATH = "vectorstore"
COLLECTION_NAME  = "hp_books"

# Chunking
CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50

# Retrieval
TOP_K_PER_SUBQUERY = 5

# Agentic loop controls
MAX_SUBQUERIES         = 4   # how many angles to break the question into
MAX_RETRIEVAL_ATTEMPTS = 2   # how many times to re-search if results are bad
RELEVANCE_THRESHOLD    = 6   # minimum acceptable quality score out of 10
