⚖️ Luke: The Supreme Court of AI
Luke is a Multi-LLM Ensemble engine designed to solve the "hallucination problem" in modern AI. Instead of trusting a single model, Luke acts as a judge, consulting the world's five most powerful AI models simultaneously to reach a verified, high-accuracy consensus.

🚀 The Core Philosophy
In high-stakes professional environments, "good enough" AI isn't good enough. Luke operates on the principle of Ensemble Reasoning:

Parallel Querying: Luke broadcasts your query to a council of 5 distinct "experts" (GPT-5, Claude, Gemini, DeepSeek, and Grok).

Consensus Analysis: Luke identifies where models agree and, more importantly, where they conflict.

Intelligent Synthesis: A "Lead Justice" model reviews the council's findings to deliver one perfected, fact-checked response.

✨ Key Features
Anti-Hallucination Engine: Automatically flags outliers and contradictions.

360-Degree Perspective: Combines real-time data (Grok/Gemini) with deep reasoning (GPT/Claude).

Professional Grade Accuracy: Designed for niches where being wrong has consequences (Legal, Research, Journalism).

Cloud Native: Powered by Streamlit for 24/7 global accessibility.

🛠️ Tech Stack
Language: Python 3.11+

Framework: Streamlit (Frontend/UI)

Orchestration: OpenRouter API (Unified LLM access)

Models: GPT-5.2, Claude 4.5 Opus, Gemini 3 Pro, DeepSeek-R1, Grok 4.1

📦 Installation & Local Setup
To run Luke on your local machine for development:

Clone the repository:

Bash

git clone https://github.com/LBDickinson/luke-ai.git
cd luke-ai
Install dependencies:

Bash

pip install -r requirements.txt
Set up your API Key: Create a .streamlit/secrets.toml file and add:

Ini, TOML

OPENROUTER_API_KEY = "your_key_here"
Run the app:

Bash

streamlit run luke.py
📈 Roadmap
[ ] Implement side-by-side "Conflict View" for professional auditing.

[ ] Add PDF/Document upload for council-based document analysis.

[ ] Integrate Stripe Pro-tier user authentication.

Created by L.B. Dickinson
