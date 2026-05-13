# ⚡ AI Prompt Evaluator & Optimizer Dashboard

> **Automated LLM Benchmarking · Structured QA · Side-by-Side Analysis**

A production-grade portfolio project demonstrating senior-level **Prompt Engineering**, **LLM Evaluation**, and **AI Quality Assurance** skills — built entirely on **free, open-access APIs**. Designed for AI training companies that need to automate prompt and agent quality assurance at scale.

---

## 🎯 What This System Does

Traditional LLM evaluation relies on subjective, manual review — slow, inconsistent, and impossible to scale. This dashboard automates the entire QA pipeline:

1. **Submit** a single test prompt via the clean Streamlit interface
2. **Simultaneously dispatch** it to Gemini (Google AI Studio) and Llama 3 (Groq Cloud) using async parallel calls
3. **Display** both responses side-by-side in a professional dual-column layout
4. **Run a third AI call** — a *Critical Evaluator* — where Gemini acts as a **neutral judge**, scoring both outputs on three structured criteria using Structured Outputs (JSON)
5. **Persist** every evaluation to a native CSV benchmark log (zero pandas dependency)
6. **Visualize** model performance trends using Streamlit's native `st.bar_chart`

---

## 🏗 Architecture

```
ai_prompt_evaluator/
│
├── app.py            # Streamlit UI — tabs, columns, charts, session state
├── evaluator.py      # Async LLM calls + neutral Gemini judge
├── history.py        # Native CSV I/O + st.cache_data caching layer
├── requirements.txt  # Minimal dependency list (3 packages)
└── prompt_benchmark_history.csv  # Auto-generated benchmark log
```

```
User Prompt
    │
    ├──► Gemini 1.5 Flash  ──────────────────────┐
    │    (google-generativeai)                    │
    │                                             ▼
    └──► Llama 3 8B via Groq  ──────► Gemini Judge (neutral)
         (groq library)                    │
                                           ▼
                                  Structured JSON Scores
                                  + CSV persistence
                                  + st.bar_chart
```

### Module Responsibilities

| File | Role |
|---|---|
| `app.py` | UI layer — renders all Streamlit components, manages `st.session_state` |
| `evaluator.py` | Business logic — async model orchestration, Gemini as neutral JSON judge |
| `history.py` | Data layer — CSV persistence, `st.cache_data` for read performance |

---

## 🧠 Key Technical Concepts

### Asynchronous Evaluation
Both model API calls (`call_gemini` and `call_llama`) are dispatched concurrently using Python's `asyncio.gather`. This eliminates sequential latency — instead of waiting for two API calls in series, both complete in the time of the slower one:

```python
gemini_resp, llama_resp = await asyncio.gather(
    call_gemini(prompt, gemini_key),
    call_llama(prompt, groq_key),
)
```

### Structured Outputs
The Critical Evaluator uses a strict system prompt that forces Gemini to return **only valid JSON** with a defined schema — no markdown, no prose, no hallucinated fields. This enables downstream programmatic processing, trend analysis, and dashboard rendering without fragile string parsing:

```json
{
  "gemini": { "clarity": 4, "technical_accuracy": 5, "instruction_alignment": 4, "feedback": "..." },
  "llama":  { "clarity": 3, "technical_accuracy": 4, "instruction_alignment": 3, "feedback": "..." },
  "winner": "gemini",
  "reasoning": "..."
}
```

### Automated Benchmarking
Every evaluation is automatically appended to `prompt_benchmark_history.csv` using Python's **native `csv` library** — zero external dependencies beyond the three packages in `requirements.txt`. The system tracks per-model scores across three axes:

| Criterion | Description |
|---|---|
| **Clarity** | Structure, readability, and logical flow of the response |
| **Technical Accuracy** | Correctness of facts, logic, and domain knowledge |
| **Instruction Alignment** | How fully the response addresses the original prompt |

Averages are recomputed on each dashboard load and surfaced as interactive bar charts — enabling data-driven decisions about which model performs best for specific task types.

### Neutral Judge Design
Gemini evaluates **both responses as anonymous "Response A" and "Response B"** — without any label indicating which model produced which output. This eliminates self-preferential bias and produces fairer, more trustworthy scores, a critical design requirement for production evaluation pipelines.

---

## 🚀 Setup on Windows (VS Code)

### Step 1 — Open Terminal in VS Code
```
Menu → Terminal → New Terminal   (or Ctrl + `)
```

### Step 2 — Create and Activate Virtual Environment
```powershell
# Create the venv
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3 — Install Dependencies
```powershell
pip install streamlit google-generativeai groq
```
Or use the requirements file:
```powershell
pip install -r requirements.txt
```

### Step 4 — Get Your Free API Keys

| Key | Source | Free Tier |
|---|---|---|
| **Gemini API Key** | [aistudio.google.com](https://aistudio.google.com) | ✅ Free |
| **Groq API Key** | [console.groq.com](https://console.groq.com) | ✅ Free |

Enter both in the app's **sidebar** at runtime — never hardcode or commit keys.

### Step 5 — Run the App
```powershell
streamlit run app.py
```
The dashboard opens automatically at `http://localhost:8501`.

---

## 📊 Performance Optimizations

| Technique | Implementation |
|---|---|
| `st.cache_data(ttl=5)` | CSV history is cached and only re-read every 5 seconds, preventing redundant I/O on each Streamlit rerun |
| `st.session_state` | Evaluation results persist across UI interactions without re-calling APIs |
| `asyncio.gather` | Parallel API dispatch eliminates sequential latency between Gemini and Llama 3 |
| No pandas | Native `csv` module keeps memory footprint minimal on 8 GB RAM machines |
| 3 dependencies only | `streamlit`, `google-generativeai`, `groq` — ultra-lightweight environment |

---

## 💼 Business Value for AI Training Companies

This system directly addresses the core QA challenges faced by teams building LLM-powered products:

- **Model Selection** — Empirically determine whether Gemini or Llama 3 performs better for specific task categories (summarization, code generation, reasoning) rather than relying on static benchmark leaderboards
- **Prompt Regression Testing** — Detect when prompt changes degrade output quality before reaching production
- **Open-Source vs Proprietary Comparison** — Maintain an auditable, time-stamped log comparing a proprietary model (Gemini) against an open-source model (Llama 3) on real production prompts
- **Agent QA Pipelines** — The evaluation pattern (structured judge + CSV log + async dispatch) extends directly to multi-agent system testing and automated red-teaming

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | Streamlit 1.35+ |
| Competitor A | Google Gemini 1.5 Flash (`google-generativeai`) |
| Competitor B | Meta Llama 3 8B via Groq Cloud (`groq`) |
| Neutral Judge | Gemini 1.5 Flash (anonymous evaluation) |
| Async Runtime | Python `asyncio` |
| Data Storage | Python native `csv` (no pandas) |
| Caching | `st.cache_data`, `st.session_state` |
| Python | 3.11+ |

---

## 📁 CSV Schema

`prompt_benchmark_history.csv` — auto-generated on first run:

| Column | Type | Description |
|---|---|---|
| `timestamp` | string | ISO datetime of evaluation |
| `prompt` | string | The test prompt submitted |
| `gemini_clarity` | float | Score 1–5 |
| `gemini_technical_accuracy` | float | Score 1–5 |
| `gemini_instruction_alignment` | float | Score 1–5 |
| `gemini_avg` | float | Mean of three Gemini scores |
| `llama_clarity` | float | Score 1–5 |
| `llama_technical_accuracy` | float | Score 1–5 |
| `llama_instruction_alignment` | float | Score 1–5 |
| `llama_avg` | float | Mean of three Llama 3 scores |
| `winner` | string | `"gemini"` \| `"llama"` \| `"tie"` |

---

## 👤 Author

Built as a portfolio demonstration of senior **LLM / Prompt Engineering** skills.
Designed to showcase expertise in: async LLM orchestration, structured output engineering, automated evaluation pipelines, neutral judge design, and production-ready Streamlit development.

---

## 📄 License

MIT — free to use, fork, and extend.