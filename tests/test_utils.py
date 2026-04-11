def test_chunk_documents():
    from app.utils import chunk_documents
    from langchain_core.documents import Document
    docs = [Document(page_content="a" * 3000, metadata={})]
    chunks = chunk_documents(docs)
    assert len(chunks) > 1
