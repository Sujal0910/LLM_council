# 🏛️ LLM Council: Multi-Agent Consensus System

Inspired by Andrej Karpathy's vision of an "LLM Council," this project is a Flask-based orchestration engine that pits multiple Large Language Models against each other to produce high-quality, peer-reviewed answers.



## 🚀 The Concept
Standard LLM responses often suffer from "single-model bias" or hallucinations. This system solves that by creating a three-phase pipeline:

1.  **Phase 1: Diverse Drafting** – Four distinct personalities (The Chairman, The Rebel, The Engineer, and The Academic) generate independent solutions.
2.  **Phase 2: Peer Review** – Every council member acts as a "harsh critic," reviewing the combined transcript for mistakes or logical fallacies.
3.  **Phase 3: The Verdict** – The Chairman (Llama 3.3) synthesizes the drafts and critiques into one final, optimized response.

## 🛠️ Tech Stack
* **Backend:** Python / Flask
* **AI Orchestration:** OpenRouter API (Accessing Llama 3.3, Grok 4.1, DeepSeek, and Trinity Mini)
* **Concurrency:** `ThreadPoolExecutor` for parallel API calls
* **Environment:** `python-dotenv` for secure secret management

## 🏗️ Key Implementation Details
* **Parallel Execution:** To avoid the latency of four sequential API calls, the system uses Python's threading to hit all models simultaneously, reducing response time by ~75%.
* **System Prompt Engineering:** Each agent has a unique persona defined in the system instructions to ensure a broad spectrum of perspectives.
* **Error Handling:** Robust try-except blocks ensure that if one model fails, the council continues its deliberation.
