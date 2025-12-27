# 🏛️ LLM Council: Multi-Agent Consensus System

Inspired by Andrej Karpathy's vision of an "LLM Council," this project is a Flask-based orchestration engine that pits multiple Large Language Models against each other to produce high-quality, peer-reviewed answers.



## 🚀 The Concept
Standard LLM responses often suffer from "single-model bias" or hallucinations. This system solves that by creating a three-phase "Agentic Pipeline":

1. **Phase 1: Diverse Drafting** – Four distinct personalities (**Llama 3.3, Grok 4.1, DeepSeek, and Trinity Mini**) generate independent solutions.
2. **Phase 2: Peer Review** – Every council member acts as a "harsh critic," reviewing the combined transcript to find mistakes or bias.
3. **Phase 3: The Verdict** – The Chairman (Llama 3.3) synthesizes the drafts and critiques into one "Perfect Answer."

## 🛠️ Tech Stack
* **Backend:** Python / Flask
* **AI Orchestration:** OpenRouter API 
* **Concurrency:** `ThreadPoolExecutor` for parallel API calls
* **Environment:** `python-dotenv` for secure secret management

## 🏗️ Key Implementation Highlights
* **Parallel Execution:** Used `ThreadPoolExecutor` to hit all APIs simultaneously, ensuring the system is 4x faster than sequential processing.
* **Persona Engineering:** Crafted specific system prompts to ensure a broad spectrum of perspectives.
* **Critique Loop:** Implemented a self-correction layer to minimize hallucinations.

## 🚦 Getting Started

### Installation
1. **Clone the repo:**
   `git clone https://github.com/Sujal0910/LLM_council.git`
2. **Setup .env:**
   Create a `.env` file and add: `OPENROUTER_API_KEY=your_key_here`
3. **Install dependencies:**
   `pip install -r requirements.txt`
4. **Run the app:**
   `python app.py`

---
*Built by [Sujal](https://github.com/Sujal0910)*
