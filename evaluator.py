import json
import concurrent.futures
from groq import Groq

def call_llama33(prompt, api_key):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        return completion.choices[0].message.content or ""
    except Exception as exc:
        return f"[Llama 3.3 Error] {exc}"

def call_llama4(prompt, api_key):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        return completion.choices[0].message.content or ""
    except Exception as exc:
        return f"[Llama 4 Error] {exc}"

EVALUATOR_SYSTEM = 'Respond ONLY with valid JSON: {"model_a":{"clarity":0,"technical_accuracy":0,"instruction_alignment":0,"feedback":""},"model_b":{"clarity":0,"technical_accuracy":0,"instruction_alignment":0,"feedback":""},"winner":"tie","reasoning":""}'

def call_evaluator(prompt, resp_a, resp_b, api_key):
    try:
        client = Groq(api_key=api_key)
        user_msg = f"Prompt:\n{prompt}\n\nRESPONSE A:\n{resp_a}\n\nRESPONSE B:\n{resp_b}\n\nReturn only JSON."
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": EVALUATOR_SYSTEM}, {"role": "user", "content": user_msg}],
            max_tokens=1024,
        )
        raw = completion.choices[0].message.content or ""
        raw = raw.strip().replace("`json","").replace("`","").strip()
        return json.loads(raw)
    except Exception as exc:
        base = {"clarity":0,"technical_accuracy":0,"instruction_alignment":0,"feedback":str(exc)}
        return {"model_a":base.copy(),"model_b":base.copy(),"winner":"tie","reasoning":str(exc)}

def run_evaluation(prompt, key_a, key_b):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        fa = executor.submit(call_llama33, prompt, key_a)
        fb = executor.submit(call_llama4, prompt, key_b)
        resp_a = fa.result()
        resp_b = fb.result()
    eval_result = call_evaluator(prompt, resp_a, resp_b, key_a)
    return {"prompt":prompt,"response_a":resp_a,"response_b":resp_b,"eval":eval_result}