# ai-prompt-evaluator
Automated LLM evaluation dashboard comparing Llama 3.3 vs Llama 4 via Groq Cloud. Features parallel inference, structured JSON scoring, and asynchronous anonymous peer evaluation to eliminate AI self-preferential bias. Built with Streamlit and native Python CSV handling.

# ⚡ AI Prompt Evaluator & Optimizer Dashboard

> **Llama 3.3 70B vs Llama 4 Scout · Anonymous Peer Evaluation · Automated Benchmarking · 100% Free APIs**

A production-grade portfolio project demonstrating senior-level **Prompt Engineering**, **LLM Evaluation**, and **AI Quality Assurance** skills — built entirely on free, open-access APIs via Groq Cloud. Designed for AI training companies that need to automate prompt and agent quality assurance at scale.

---

## 🎯 What This System Does

Traditional LLM evaluation relies on subjective, manual review — slow, inconsistent, and impossible to scale. This dashboard automates the entire QA pipeline:

1. **Submit** a single test prompt via the clean Streamlit interface
2. **Simultaneously dispatch** it to Llama 3.3 70B and Llama 4 Scout using parallel threads
3. **Display** both responses side-by-side in a professional dual-column layout
4. **Run a third AI call** — a Critical Evaluator — where Llama 3.3 70B acts as a neutral anonymous judge, scoring both outputs on three structured criteria using Structured Outputs (JSON)
5. **Persist** every evaluation to a native CSV benchmark log (zero pandas dependency)
6. **Visualize** model performance trends using Streamlit's native `st.bar_chart`

---

## 🏆 Key Feature: Anonymous Peer Evaluation

This project implements **Anonymous Peer Evaluation** — the same methodology used in academic peer review and professional LLM research benchmarks like [LMSYS Chatbot Arena](https://chat.lmsys.org/).

The neutral judge receives both responses labeled only as **"Response A"** and **"Response B"** — with **zero information about which model produced which answer**:

```python
user_msg = f"Prompt:\n{prompt}\n\nRESPONSE A:\n{resp_a}\n\nRESPONSE B:\n{resp_b}\n\nReturn only JSON."
```

### Why this matters
- **Eliminates self-preferential bias** — the judge cannot favor a model it knows by name
- **Research-grade fairness** — scores reflect actual output quality, not model reputation
- **Production-ready pattern** — directly applicable to multi-agent QA pipelines and automated red-teaming

---

## 🏗 Architecture

```
ai-prompt-evaluator/
│
├── app.py                        # Streamlit UI — tabs, columns, charts, session state
├── evaluator.py                  # Parallel model calls + anonymous neutral judge
├── history.py                    # Native CSV I/O + st.cache_data caching layer
├── requirements.txt              # 2 dependencies only
└── prompt_benchmark_history.csv  # Auto-generated benchmark log
```

```
User Prompt
    │
    ├──► Llama 3.3 70B (Groq) ──────────────────┐
    │                                             │
    │                                             ▼
    └──► Llama 4 Scout (Groq) ──────► Llama 3.3 Judge (neutral)
                                           │
                                           ▼
                                  Structured JSON Scores
                                  + CSV persistence
                                  + st.bar_chart
```

### Module Responsibilities

| File | Role |
|---|---|
| `app.py` | UI layer — renders all Streamlit components, manages `st.session_state` |
| `evaluator.py` | Business logic — parallel model calls, Llama 3.3 as anonymous neutral judge |
| `history.py` | Data layer — CSV persistence, `st.cache_data` for read performance |

---

## 🧠 Key Technical Concepts

### Anonymous Peer Evaluation
The judge model (Llama 3.3 70B) evaluates responses without knowing their origin — eliminating bias and producing fairer, research-grade scores. Responses are passed as anonymous "Response A" and "Response B".

### Parallel Evaluation
Both model calls are dispatched simultaneously using `concurrent.futures.ThreadPoolExecutor` — fully compatible with Streamlit's event loop, no asyncio conflicts:

```python
with ThreadPoolExecutor(max_workers=2) as executor:
    fa = executor.submit(call_llama33, prompt, key_a)
    fb = executor.submit(call_llama4,  prompt, key_b)
    resp_a = fa.result()
    resp_b = fb.result()
```

### Structured Outputs
The Critical Evaluator uses a strict system prompt that forces the judge to return **only valid JSON** with a defined schema — no markdown, no prose, no hallucinated fields:

```json
{
  "model_a": {"clarity": 4, "technical_accuracy": 5, "instruction_alignment": 4, "feedback": "..."},
  "model_b": {"clarity": 3, "technical_accuracy": 4, "instruction_alignment": 3, "feedback": "..."},
  "winner": "model_a",
  "reasoning": "..."
}
```

### Automated Benchmarking
Every evaluation is automatically appended to `prompt_benchmark_history.csv` using Python's **native `csv` library** — zero external dependencies beyond the two packages in `requirements.txt`. The system tracks per-model scores across three axes:

| Criterion | Description |
|---|---|
| **Clarity** | Structure, readability, and logical flow of the response |
| **Technical Accuracy** | Correctness of facts, logic, and domain knowledge |
| **Instruction Alignment** | How fully the response addresses the original prompt |

---

## 🚀 Setup on Windows (VS Code)

### Step 1 — Open Terminal in VS Code
```
Menu → Terminal → New Terminal   (or Ctrl + `)
```

### Step 2 — Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3 — Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4 — Get Your Free Groq API Key

| Key | Source | Free Tier |
|---|---|---|
| **Groq API Key** | [console.groq.com](https://console.groq.com) | ✅ Free |

Enter the key in both sidebar fields at runtime — never hardcode or commit keys.

### Step 5 — Run the App
```powershell
streamlit run app.py
```

The dashboard opens automatically at `http://localhost:8501`.

---

## 📊 Performance Optimizations

| Technique | Implementation |
|---|---|
| `concurrent.futures.ThreadPoolExecutor` | Parallel API dispatch — both models called simultaneously |
| `st.cache_data(ttl=5)` | CSV history cached, re-read only every 5 seconds |
| `st.session_state` | Results persist across UI interactions without re-calling APIs |
| No pandas | Native `csv` module — minimal memory footprint on 8 GB RAM machines |
| 2 dependencies only | `streamlit` and `groq` — ultra-lightweight environment |

---

## 💼 Business Value for AI Training Companies

- **Model Generation Comparison** — Empirically measure Llama 3.3 vs Llama 4 on your specific task categories (summarization, code generation, reasoning) rather than relying on static benchmark leaderboards
- **Prompt Regression Testing** — Detect when prompt changes degrade output quality before reaching production
- **Open-Source Benchmarking** — Maintain an auditable, time-stamped log comparing two generations of the same model family on real production prompts
- **Agent QA Pipelines** — The evaluation pattern (anonymous judge + CSV log + parallel dispatch) extends directly to multi-agent system testing and automated red-teaming

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | Streamlit 1.35+ |
| Competitor A | Meta Llama 3.3 70B Versatile via Groq Cloud |
| Competitor B | Meta Llama 4 Scout 17B via Groq Cloud |
| Anonymous Judge | Meta Llama 3.3 70B Versatile via Groq Cloud |
| Parallel Runtime | Python `concurrent.futures.ThreadPoolExecutor` |
| Data Storage | Python native `csv` (no pandas) |
| Caching | `st.cache_data`, `st.session_state` |
| Python | 3.8+ |

---

## 📁 CSV Schema

`prompt_benchmark_history.csv` — auto-generated on first run:

| Column | Type | Description |
|---|---|---|
| `timestamp` | string | ISO datetime of evaluation |
| `prompt` | string | The test prompt submitted |
| `model_a_clarity` | float | Llama 3.3 clarity score 1–5 |
| `model_a_technical_accuracy` | float | Llama 3.3 technical accuracy 1–5 |
| `model_a_instruction_alignment` | float | Llama 3.3 instruction alignment 1–5 |
| `model_a_avg` | float | Llama 3.3 mean score |
| `model_b_clarity` | float | Llama 4 clarity score 1–5 |
| `model_b_technical_accuracy` | float | Llama 4 technical accuracy 1–5 |
| `model_b_instruction_alignment` | float | Llama 4 instruction alignment 1–5 |
| `model_b_avg` | float | Llama 4 mean score |
| `winner` | string | `"model_a"` \| `"model_b"` \| `"tie"` |

---

## 🚢 Deploying to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub and select this repo
4. Add your Groq key under **Settings → Secrets**:

```toml
GROQ_KEY = "gsk_..."
```

> Note: The CSV benchmark history resets when the app restarts on the free tier. For persistent storage, replace the CSV with a free database like Supabase.

---

## 👤 Author

Built as a portfolio demonstration of senior **LLM / Prompt Engineering** skills.
Showcases: anonymous peer evaluation, parallel LLM orchestration, structured output engineering, automated benchmarking pipelines, and production-ready Streamlit development.

---

## 📄 License

MIT — free to use, fork, and extend.
