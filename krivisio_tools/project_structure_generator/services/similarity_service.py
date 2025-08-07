from typing import List, Dict
import hashlib
import numpy as np
from openai import OpenAI
from krivisio_tools.report_generation.app.core.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


# Example in-memory project example store
SIMILAR_PROJECTS_DB: List[Dict] = []


def get_embedding(text: str) -> List[float]:
    """
    Uses OpenAI Embedding API to get a vector representation of text.

    Args:
        text (str): Input string.

    Returns:
        List[float]: Embedding vector.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[text.strip()]
    )
    return response.data[0].embedding


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Computes cosine similarity between two vectors.

    Returns:
        float: Similarity score between -1 and 1.
    """
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def find_similar_examples(
    input_description: str,
    top_k: int = 3
) -> List[Dict]:
    """
    Finds similar project examples from the local DB based on description.

    Args:
        input_description (str): New project description.
        top_k (int): Number of similar examples to return.

    Returns:
        List[Dict]: Top similar examples with structure and metadata.
    """
    input_vec = get_embedding(input_description)

    scored_projects = []
    for project in SIMILAR_PROJECTS_DB:
        example_vec = project.get("embedding")
        if not example_vec:
            continue
        similarity = cosine_similarity(input_vec, example_vec)
        scored_projects.append((similarity, project))

    # Sort by highest similarity
    scored_projects.sort(key=lambda x: x[0], reverse=True)

    # Return top-K examples
    return [p[1] for p in scored_projects[:top_k]]


def add_example_to_db(description: str, structure: Dict) -> None:
    """
    Adds a new example to the in-memory project DB.

    Args:
        description (str): Project description.
        structure (dict): Associated directory structure.
    """
    embedding = get_embedding(description)
    SIMILAR_PROJECTS_DB.append({
        "description": description,
        "structure": structure,
        "embedding": embedding
    })
