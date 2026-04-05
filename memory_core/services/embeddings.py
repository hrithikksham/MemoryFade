from sentence_transformers import SentenceTransformer

# Load models once (avoid reloading every request)
MODELS = {
    "minilm": SentenceTransformer("all-MiniLM-L6-v2"),
    "mxbai": SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")
}

# Map full names → short keys so both formats work
MODEL_ALIASES = {
    "all-MiniLM-L6-v2": "minilm",
    "mxbai-embed-large": "mxbai",
    "mixedbread-ai/mxbai-embed-large-v1": "mxbai",
    "minilm": "minilm",
    "mxbai": "mxbai"
}

def generate_embedding(
    text: str,
    model_name: str = "mxbai"
) -> list[float]:
    resolved = MODEL_ALIASES.get(model_name)

    if resolved is None:
        raise ValueError(
            f"Unsupported embedding model: {model_name}. "
            f"Valid options: {list(MODEL_ALIASES.keys())}"
        )

    embedding = MODELS[resolved].encode(text)
    return embedding.tolist()