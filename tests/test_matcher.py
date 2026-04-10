import pytest
from unittest.mock import Mock
from app.matcher import ResumeMatcher


@pytest.fixture
def mock_vector_store():
    store = Mock()
    store.similarity_search.return_value = [
        Mock(page_content="Python expert", metadata={"source": "resume1.pdf"}),
        Mock(page_content="Java dev", metadata={"source": "resume2.pdf"}),
    ]
    return store


def test_rank_resumes(mock_vector_store):
    matcher = ResumeMatcher(mock_vector_store)
    results = matcher.rank_resumes("Need Python")
    assert len(results) == 2
    assert results[0]["resume"] == "resume1.pdf"
