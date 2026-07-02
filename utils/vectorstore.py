from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

def create_retriever(transcript, embeddings):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.create_documents([transcript])

    vector_store = FAISS.from_documents(
        docs,
        embeddings
    )

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k":4}
    )