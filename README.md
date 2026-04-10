# llm-resume-ranker

A simple AI-powered resume screener.  
Built with LangChain, FAISS, and Streamlit.

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![CI](https://github.com/besmaguesmi/llm-resume-ranker/actions/workflows/ci.yml/badge.svg)](https://github.com/besmaguesmi/llm-resume-ranker/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)](https://hub.docker.com/)

## Features

- Upload PDF resumes & paste job description
- Rank candidates using semantic search (FAISS + sentence-transformers)
- Generate candidate summaries with Hugging Face LLM (flan-t5-large)
- Streamlit UI with expandable cards
- Unit tests, GitHub Actions CI, Docker support

## Quick Start

### Project structure
```
.
├── app/
│   ├── main.py               # Streamlit entrypoint
│   ├── config.py             # HF token, model names
│   ├── utils.py              # PDF loading, chunking
│   ├── resume_processor.py   # FAISS indexing with HF embeddings
│   ├── matcher.py            # Ranking & summarization
│   └── ui.py                 # Streamlit UI components
├── tests/                    # Unit tests
├── .github/workflows/ci.yml  # GitHub Actions
├── Dockerfile
├── requirements.txt
└── README.md
```

### Prerequisites
- Python 3.10+
- [Hugging Face account](https://huggingface.co/join) and an API token ([get it here](https://huggingface.co/settings/tokens))

### Setup

```
git clone https://github.com/YOUR_USERNAME/llm-resume-ranker.git
cd llm-resume-ranker
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip3 install -r requirements.txt
cp .env.example .env
```

### Run App
#### Without Docker
```
streamlit run app/main.py
# or
python3 -m streamlit run app/main.py
```
Open http://localhost:8501

Run tests
```
pip3 install -r requirements-dev.txt
python3 -m pytest tests/
```

#### With Docker
```
docker build -t resume-screener .
docker run -p 8501:8501 --env-file .env resume-screener
```
