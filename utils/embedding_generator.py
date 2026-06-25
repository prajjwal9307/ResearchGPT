from sentence_transformers import (
    SentenceTransformer
)

model = SentenceTransformer(
    "BAAI/bge-base-en-v1.5"
)


def generate_embeddings(chunks):

    texts = []

    for chunk in chunks:
        texts.append(chunk["text"])

    embeddings = model.encode(texts, normalize_embeddings=True)

    return embeddings


def generate_query_embedding(query):

    embedding = model.encode(query)

    return embedding