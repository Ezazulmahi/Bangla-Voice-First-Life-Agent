import hashlib
import math
import re

EMBEDDING_DIM = 256


def embed_text(text: str, dim: int = EMBEDDING_DIM) -> list[float]:
    """Deterministic hashing-based bag-of-words embedding (the "hashing
    trick"). This is a placeholder for a real embedding model: Groq (our LLM
    provider) doesn't expose an embeddings endpoint, and pulling in a local
    model (sentence-transformers/torch) is too heavy for this MVP. It's
    enough to make explain_process's RAG retrieval functional over a small
    seeded corpus — swap for a real embedding model before relying on it at
    scale.
    """
    vec = [0.0] * dim
    for token in re.findall(r"\w+", text.lower()):
        idx = int(hashlib.md5(token.encode()).hexdigest(), 16) % dim
        vec[idx] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))
