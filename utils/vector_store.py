import chromadb
import uuid
from rank_bm25 import BM25Okapi

client = chromadb.PersistentClient(
    path="vectorstore"
)

collection = client.get_or_create_collection(
    name="research_papers"
)


def store_embeddings(
        chunks,
        embeddings
):

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        ids.append(
            str(uuid.uuid4())
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            {
                "page_number":
                    chunk["page_number"],

                "file_name":
                    chunk["file_name"],

                "session":
                    chunk["session"]
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


# Hybrid

def retrieve_relevant_chunks(
        query,
        query_embedding,
        session_name,
        top_k=20
):

    # -------------------------
    # Dense Search
    # -------------------------

    dense_results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k,
        where={
            "session": session_name
        }
    )

    dense_documents = (
        dense_results["documents"][0]
    )

    dense_metadatas = (
        dense_results["metadatas"][0]
    )

    # -------------------------
    # BM25 Search
    # -------------------------

    all_docs = collection.get(
        where={
            "session": session_name
        }
    )

    corpus = all_docs["documents"]

    tokenized_corpus = [
        doc.split()
        for doc in corpus
    ]

    bm25 = BM25Okapi(
        tokenized_corpus
    )

    tokenized_query = query.split()

    scores = bm25.get_scores(
        tokenized_query
    )

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:20]

    bm25_documents = []

    for idx in ranked_indices:
        bm25_documents.append(
            corpus[idx]
        )

    # -------------------------
    # Hybrid Merge
    # -------------------------

    final_documents = list(
        set(
            dense_documents +
            bm25_documents
        )
    )

    metadata_map = {}

    for doc, meta in zip(
            dense_documents,
            dense_metadatas):

        metadata_map[doc] = meta

    return {
        "documents": final_documents,
        "metadata_map": metadata_map
    }


