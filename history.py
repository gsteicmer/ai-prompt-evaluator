import csv
import os
import streamlit as st
from datetime import datetime
from typing import List, Dict, Any

CSV_FILE = "prompt_benchmark_history.csv"

FIELDNAMES = [
    "timestamp","prompt",
    "model_a_clarity","model_a_technical_accuracy","model_a_instruction_alignment","model_a_avg",
    "model_b_clarity","model_b_technical_accuracy","model_b_instruction_alignment","model_b_avg",
    "winner",
]

NUMERIC_FIELDS = [
    "model_a_clarity","model_a_technical_accuracy","model_a_instruction_alignment","model_a_avg",
    "model_b_clarity","model_b_technical_accuracy","model_b_instruction_alignment","model_b_avg",
]

def _ensure_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()

def save_result(prompt, model_a_scores, model_b_scores, winner):
    _ensure_csv()
    criteria = ["clarity","technical_accuracy","instruction_alignment"]
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt.replace("\n"," ").strip(),
        "model_a_clarity": model_a_scores.get("clarity",0),
        "model_a_technical_accuracy": model_a_scores.get("technical_accuracy",0),
        "model_a_instruction_alignment": model_a_scores.get("instruction_alignment",0),
        "model_a_avg": round(sum(model_a_scores.get(c,0) for c in criteria)/3,3),
        "model_b_clarity": model_b_scores.get("clarity",0),
        "model_b_technical_accuracy": model_b_scores.get("technical_accuracy",0),
        "model_b_instruction_alignment": model_b_scores.get("instruction_alignment",0),
        "model_b_avg": round(sum(model_b_scores.get(c,0) for c in criteria)/3,3),
        "winner": winner,
    }
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow(row)

@st.cache_data(ttl=5)
def load_history():
    _ensure_csv()
    rows = []
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                for key in NUMERIC_FIELDS:
                    try:
                        row[key] = float(row[key])
                    except (ValueError, KeyError):
                        row[key] = 0.0
                rows.append(dict(row))
    except FileNotFoundError:
        pass
    return rows

def compute_averages(history):
    if not history:
        return {}
    n = len(history)
    return {
        "model_a_avg": round(sum(r["model_a_avg"] for r in history)/n,2),
        "model_b_avg": round(sum(r["model_b_avg"] for r in history)/n,2),
        "model_a_clarity_avg": round(sum(r["model_a_clarity"] for r in history)/n,2),
        "model_a_technical_accuracy_avg": round(sum(r["model_a_technical_accuracy"] for r in history)/n,2),
        "model_a_instruction_alignment_avg": round(sum(r["model_a_instruction_alignment"] for r in history)/n,2),
        "model_b_clarity_avg": round(sum(r["model_b_clarity"] for r in history)/n,2),
        "model_b_technical_accuracy_avg": round(sum(r["model_b_technical_accuracy"] for r in history)/n,2),
        "model_b_instruction_alignment_avg": round(sum(r["model_b_instruction_alignment"] for r in history)/n,2),
    }
