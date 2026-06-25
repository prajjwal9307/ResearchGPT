from langchain_experimental.text_splitter import SemanticChunker 
from langchain_community.embeddings import (HuggingFaceEmbeddings)

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

text_splitter = SemanticChunker(
    embeddings=embedding_model,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95
)

def chunk_text(pages,session_name):
    all_chunks=[]
    for page in pages:
        page_number=page["page_number"]
        file_name=page["file_name"]
        chunks=text_splitter.split_text(page["text"])

        for chunk in chunks:
            all_chunks.append(
                {
                    "text":chunk,
                    "page_number":page_number,
                    "file_name":file_name,
                    "session":session_name
                }
            )
        
    
    return all_chunks
