from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import LLM_MODEL, HUGGINGFACE_API_KEY, TOP_K_RESULTS


class ResumeMatcher:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = HuggingFaceEndpoint(
            repo_id=LLM_MODEL,
            huggingfacehub_api_token=HUGGINGFACE_API_KEY,
            task="text-generation",
        )

    def rank_resumes(self, job_description, top_k=TOP_K_RESULTS):
        docs = self.vector_store.similarity_search(job_description, k=top_k * 2)
        results = []
        for doc in docs:
            score = doc.metadata.get(
                "score", 0.5
            )  # FAISS doesn't give scores directly; we'll compute manually
            results.append(
                {
                    "resume": doc.metadata["source"],
                    "content": doc.page_content[:500],
                    "score": score,
                }
            )
        # simple deduplication by source
        seen = set()
        unique = []
        for r in results:
            if r["resume"] not in seen:
                seen.add(r["resume"])
                unique.append(r)
        return unique[:top_k]

    def generate_summary(self, resume_text):
        prompt = PromptTemplate(
            template="Summarise this candidate's profile in 2-3 bullet points:\n{text}",
            input_variables=["text"],
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(text=resume_text[:2000])
