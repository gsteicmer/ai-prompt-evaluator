import streamlit as st
import json
import traceback
 
st.set_page_config(
    page_title="AI Prompt Evaluator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
try:
    from evaluator import run_evaluation
except Exception:
    st.error("IMPORT ERROR in evaluator.py")
    st.code(traceback.format_exc())
    st.stop()
 
try:
    from history import save_result, load_history, compute_averages
except Exception:
    st.error("IMPORT ERROR in history.py")
    st.code(traceback.format_exc())
    st.stop()
 
if "results" not in st.session_state:
    st.session_state.results = None
 
with st.sidebar:
    st.title("⚙️ Configuration")
    st.divider()
    key_a = st.text_input("Llama 3.3 API Key (Groq)", type="password", placeholder="gsk_...", help="Free key from console.groq.com")
    key_b = st.text_input("Llama 4 API Key (Groq)", type="password", placeholder="gsk_...", help="Free key from console.groq.com")
    st.divider()
    st.caption("Model A: Llama 3.3 70B Versatile")
    st.caption("Model B: Llama 4 Scout 17B")
    st.caption("Judge: Llama 3.3 70B (neutral)")
    st.caption("Criteria: Clarity · Technical Accuracy · Instruction Alignment")
    st.caption("Storage: Native CSV — no pandas")
 
st.title("⚡ AI Prompt Evaluator & Optimizer")
st.caption("Llama 3.3 vs Llama 4 Scout · Anonymous Peer Evaluation · Automated Benchmarking")
st.divider()
 
tab_eval, tab_history = st.tabs(["🔬 Evaluation Lab", "📊 Benchmark History"])
 
with tab_eval:
    st.subheader("📝 Test Prompt")
    prompt_text = st.text_area("prompt", height=120, placeholder="e.g. Explain gradient descent in simple terms, then write a Python implementation...", label_visibility="collapsed")
    col_btn, col_warn = st.columns([1, 3])
    with col_btn:
        run_btn = st.button("▶ Run Evaluation", type="primary", use_container_width=True)
    with col_warn:
        if not key_a or not key_b:
            st.warning("Add both API keys in the sidebar first.")
    if run_btn:
        if not prompt_text.strip():
            st.error("Please enter a prompt.")
        elif not key_a or not key_b:
            st.error("Both API keys are required.")
        else:
            try:
                with st.spinner("Sending prompt to Llama 3.3 & Llama 4 Scout simultaneously..."):
                    results = run_evaluation(prompt_text, key_a, key_b)
                st.session_state.results = results
                save_result(
                    prompt=prompt_text,
                    model_a_scores=results["eval"]["model_a"],
                    model_b_scores=results["eval"]["model_b"],
                    winner=results["eval"].get("winner", "tie"),
                )
                st.success("✅ Evaluation complete — saved to benchmark history.")
            except Exception:
                st.error("Error during evaluation:")
                st.code(traceback.format_exc())
 
    if st.session_state.results:
        r = st.session_state.results
        eval_data = r["eval"]
        winner = eval_data.get("winner", "tie")
        st.divider()
        st.subheader("🤖 Model Responses")
        col_g, col_l = st.columns(2)
        with col_g:
            st.markdown("**🏆 LLAMA 3.3 70B — WINNER**" if winner == "model_a" else "**LLAMA 3.3 70B**")
            st.info(r["response_a"])
        with col_l:
            st.markdown("**🏆 LLAMA 4 SCOUT — WINNER**" if winner == "model_b" else "**LLAMA 4 SCOUT**")
            st.info(r["response_b"])
        st.divider()
        st.subheader("🧠 Critical Evaluator Scores")
        st.caption("Anonymous judge: Llama 3.3 70B evaluated both responses without knowing which model produced which.")
        criteria = ["clarity", "technical_accuracy", "instruction_alignment"]
        labels = ["Clarity", "Technical Accuracy", "Instruction Alignment"]
        col_sg, col_sl = st.columns(2)
        for col, model_key, title in [(col_sg, "model_a", "LLAMA 3.3 70B"), (col_sl, "model_b", "LLAMA 4 SCOUT")]:
            with col:
                scores = eval_data.get(model_key, {})
                avg = round(sum(scores.get(c, 0) for c in criteria) / 3, 2)
                st.markdown(f"**{title} — Avg: {avg} / 5**")
                for c, lbl in zip(criteria, labels):
                    st.metric(label=lbl, value=f"{scores.get(c, 0)} / 5")
                st.caption(scores.get("feedback", "No feedback available."))
        if eval_data.get("reasoning"):
            st.divider()
            st.markdown(f"**Evaluator reasoning:** {eval_data['reasoning']}")
        with st.expander("🔍 Full JSON output"):
            st.code(json.dumps(eval_data, indent=2), language="json")
 
with tab_history:
    st.subheader("📊 Benchmark History")
    st.caption("Average scores per model across all recorded evaluations.")
    try:
        history = load_history()
    except Exception:
        st.error("Error loading history:")
        st.code(traceback.format_exc())
        history = []
    if not history:
        st.info("No history yet. Run your first evaluation in the Evaluation Lab tab.")
    else:
        averages = compute_averages(history)
        avg_a = averages.get("model_a_avg", 0)
        avg_b = averages.get("model_b_avg", 0)
        leader = "Llama 3.3 70B" if avg_a >= avg_b else "Llama 4 Scout"
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Evaluations", len(history))
        c2.metric("Llama 3.3 Avg", f"{avg_a:.2f}")
        c3.metric("Llama 4 Avg", f"{avg_b:.2f}")
        c4.metric("Overall Leader", leader)
        st.divider()
        st.markdown("#### 📈 Average Score Per Run")
        st.bar_chart(
            {"Llama 3.3": [r["model_a_avg"] for r in history], "Llama 4": [r["model_b_avg"] for r in history]},
            color=["#34d399", "#fb923c"],
        )
        st.markdown("#### 🔬 Criteria Breakdown (All-Time Averages)")
        keys = ["clarity", "technical_accuracy", "instruction_alignment"]
        n = len(history)
        st.bar_chart(
            {
                "Llama 3.3": [round(sum(r[f"model_a_{k}"] for r in history) / n, 2) for k in keys],
                "Llama 4":   [round(sum(r[f"model_b_{k}"] for r in history) / n, 2) for k in keys],
            },
            color=["#34d399", "#fb923c"],
        )
        st.markdown("#### 🗂 Raw Evaluation Log")
        with st.expander("Show all records"):
            header = ["Timestamp", "Prompt", "Llama 3.3 Avg", "Llama 4 Avg", "Winner"]
            table = "| " + " | ".join(header) + " |\n"
            table += "| " + " | ".join(["---"] * len(header)) + " |\n"
            for row in history:
                p = row["prompt"][:80] + "..." if len(row["prompt"]) > 80 else row["prompt"]
                table += f'| {row["timestamp"]} | {p} | {row["model_a_avg"]} | {row["model_b_avg"]} | {row["winner"]} |\n'
            st.markdown(table)