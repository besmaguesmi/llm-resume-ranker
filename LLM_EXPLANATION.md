# How the Resume Screener Works (For LLM Beginners)

This document explains the core AI concepts behind the **llm-resume-ranker** application. You don't need to be an expert – we'll break down everything from embeddings to similarity search to LLM summarization.

## What is an LLM?

**LLM** stands for **Large Language Model**. It's a type of AI trained on massive amounts of text (books, websites, articles). LLMs can understand, generate, and summarize human-like text. Examples: GPT-4, Llama, Flan-T5 (which we use here).

In this app, we use an LLM for **one specific task**: summarizing a candidate's resume into 2–3 bullet points.

## How does the app find matching resumes?

The magic happens in three steps:

### 1. Turning text into numbers – Embeddings

Computers don't understand words directly. We convert text into **vectors** (lists of numbers) using a model called **sentence-transformers/all-MiniLM-L6-v2**.

- Each resume chunk (about 1000 characters) becomes a **384‑dimensional vector** (a list of 384 numbers).
- The job description also becomes a vector of the same size.

Why do this? Because similar meanings produce similar vectors. For example:

> "Python developer with 5 years of experience"  
> and  
> "Senior Python programmer, 5 yrs"  

will have vectors that are very **close together** mathematically.

### 2. Storing vectors for fast search – FAISS

We store all resume vectors in a special database called **FAISS** (Facebook AI Similarity Search). FAISS is optimized to find the nearest vectors to a query very quickly – even with thousands of resumes.

Think of it like an index in the back of a book: instead of reading every page, you jump directly to the relevant sections.

### 3. Measuring similarity – Cosine Similarity

When you paste a job description, the app:
- Converts it into a vector using the same embedding model.
- Asks FAISS: *"Which resume vectors are closest to this job description vector?"*
- FAISS returns the most similar chunks using **cosine similarity** (a score from 0 to 1, where 1 means identical meaning).

The resumes with the highest scores are ranked at the top.

## How does summarization work?

After ranking, you can click **"Summarize"** on any candidate. The app sends a small portion of the resume text (first 1500 characters) to a free LLM hosted by Hugging Face: **google/flan-t5-large**.


The LLM generates a short, readable summary. This helps HR quickly see if the candidate matches the job without reading the entire PDF.

## Putting it all together: The RAG pattern

This app follows a popular AI pattern called **RAG** (Retrieval-Augmented Generation).

| Step | What happens | Why |
|------|--------------|-----|
| **Retrieval** | FAISS finds resume chunks similar to the job description | Find relevant information |
| **Augmentation** | We add the retrieved text to a prompt | Give context to the LLM |
| **Generation** | The LLM produces a summary or answer | Human‑readable output |

RAG is powerful because the LLM doesn't need to know anything about the candidates – it only summarizes what we give it. This reduces hallucinations (making up facts) and keeps the information accurate.

## Why did we choose these specific tools?

| Tool | Purpose | Why not something else? |
|------|---------|--------------------------|
| **sentence-transformers/all-MiniLM-L6-v2** | Embeddings (text → numbers) | Free, runs locally, no API key, good quality/speed balance |
| **FAISS** | Vector search | Fast, open‑source, widely used |
| **Flan-T5-large** | Summarization | Free via Hugging Face inference API, good for short text |
| **Streamlit** | User interface | Simplest way to build a Python web app |
| **LangChain** | Orchestration | Makes it easy to chain prompts, models, and retrievers |

## Try it yourself (no code required)

1. Upload two PDF resumes: one for a Python developer, one for a chef.
2. Paste a job description: *"Looking for a Python backend engineer with FastAPI experience."*
3. The app will rank the Python resume higher because its vectors are closer to the job description.
4. Click "Summarize" on the Python resume – the LLM will generate bullet points like:
   - *5 years of Python experience*
   - *Built REST APIs with FastAPI*
   - *Worked with PostgreSQL*

##  Further learning

- [Embeddings explained visually](https://developers.google.com/machine-learning/crash-course/embeddings/translating-to-a-lower-dimensional-space)
- [What is RAG? (easy video)](https://www.youtube.com/watch?v=T-D1OfcDW1c)
- [LangChain for beginners](https://python.langchain.com/docs/get_started/introduction)
- [Hugging Face course](https://huggingface.co/learn/nlp-course/chapter1/1?fw=pt)

## Common questions

**Q: Does the app store my resumes or job descriptions anywhere?**  
A: No. Everything stays on your local machine. The only external call is to Hugging Face for summarization (and you can disable that by removing the "Summarize" button).

**Q: Can I run this without an internet connection?**  
A: Partially. Embeddings (FAISS) work offline. Summarization requires internet unless you switch to a local LLM like Ollama.

**Q: How accurate is the ranking?**  
A: It's a good starting point, but not perfect. The simple similarity score we use doesn't account for factors like years of experience or specific certifications. You can improve it by adding a cross‑encoder model or rule‑based scoring.

**Q: Can I use OpenAI instead of Hugging Face?**  
A: Yes. The original version used OpenAI. See the GitHub history or modify `config.py` to switch back.

**Q: Why do we split resumes into chunks?**  
A: LLMs and embedding models have a maximum input length (usually 512–2048 tokens). Chunking ensures we don't lose information from long resumes. It also helps FAISS find the most relevant *section* of a resume, not just the whole document.

---

Happy screening! :)
