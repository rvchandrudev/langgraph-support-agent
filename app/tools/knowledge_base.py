from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os

from app.config import settings

_embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-l6-v2")
_vectorstore = None

def _get_vectorstore():
    """Lazy load the vectore store. Indexes the knowledge base on the first call"""
    global _vectorstore
    if _vectorstore is None:
        kb_path = os.path.join(os.path.dirname(__file__), "..", "..","data", "knowledge_base.txt")

        kb_path = os.path.abspath(kb_path)

        loader = TextLoader(kb_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 300,
            chunk_overlap = 50
        )

        chunks = text_splitter.split_documents(documents)

        _vectorstore = Chroma(
            collection_name="support_knowledge",
            embedding_function=_embedding_model,
            persist_directory="./chroma_db",
        )

        _vectorstore.add_documents(chunks)

        return _vectorstore

def search_knowledge_base(query: str) -> str:
    """
    Search the support knowledge base for relevant articles.
    Returns the top matching content.
    """
    vectorestore = _get_vectorstore()
    retriever = vectorestore.as_retriever(search_kwargs={
        "k": settings.top_k
    })

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant articles found"

    results = []
    for i, doc in enumerate(docs,1):
        results.append(f"Article {i}:\n{doc.page_content}")

    return "\n\n---\n\n".join(results)