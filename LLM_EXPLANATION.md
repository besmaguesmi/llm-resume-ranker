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

The prompt we use is:
