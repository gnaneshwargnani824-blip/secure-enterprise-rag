# Secure Enterprise RAG

Read START_HERE.md first. Windows research demo with Streamlit, Python, local TF-IDF retrieval, synthetic company documents, three simulated accounts, four authorization modes, and an OpenAI-compatible text-generation adapter.

Files: app.py (interface), core.py (retrieval/authorization/API), evaluate.py (experiments), analyze.py (descriptive summaries), test_core.py (checks), data/documents.json (15 documents), data/cases.json (90 cases), RESEARCH_PLAN.md (method and paper outline), START_HERE.md (Windows setup).

A/B deliberately expose restricted synthetic evidence to demonstrate unsafe baselines. C/D enforce document permissions in code before generation. No real authentication, caches, shared conversation history, or action-taking agents. Short documents each act as a single chunk. Role selection is a local simulation. Missing ACLs and unknown users deny access. Neither model behavior nor this prototype is a guarantee of production security.

Offline previews are never LLM performance results. Live API behavior must be validated on your laptop. Provider keys, model access, and endpoint compatibility are not verified by this package.

Suggested next research extension: neural embeddings as a second fixed retriever, authenticated identity, user-level permissions, chunk-level ACLs, and adversarial paraphrases. The current experiment isolates authorization placement using a simple reproducible lexical retriever.
