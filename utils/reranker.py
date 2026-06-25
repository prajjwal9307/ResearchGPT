from sentence_transformers import CrossEncoder
reranker_model=CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_documents(query,documents,top_k=5):
    pairs=[]
    for doc in documents:
        pairs.append((query,doc))
    
    scores=reranker_model.predict(pairs)

    scores_docs=list(zip(documents,scores))
    scores_docs.sort(key=lambda x:x[1],reverse=True)
    reranked_docs=[]
    for doc,score in scores_docs[:top_k]:
        reranked_docs.append(doc)
    
    return reranked_docs


    
