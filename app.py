from flask import Flask, render_template, request, jsonify
import json, os
from openai import OpenAI

app = Flask(__name__)
FILE = "scores.json"

def load_scores():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_scores(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/scores", methods=["GET"])
def get_scores():
    return jsonify(load_scores())

@app.route("/api/scores", methods=["POST"])
def add_score():
    body = request.get_json()
    print("DEBUG received body:", body)
    test   = (body.get("test") or "").strip()
    math   = body.get("math")
    rw     = body.get("rw")
    note   = (body.get("note") or "").strip()
    api_key = (body.get("api_key") or "").strip()

    if not test:
        return jsonify({"error": "Test name is required."}), 400

    try:
        math = int(math)
        rw   = int(rw)
    except (TypeError, ValueError):
        return jsonify({"error": "Math and R&W scores must be numbers."}), 400

    # SAT section scores: 200–800 each
    if not (200 <= math <= 800 and 200 <= rw <= 800):
        return jsonify({"error": "Each section score must be between 200 and 800."}), 400

    total = math + rw

    entry = {"test": test, "math": math, "rw": rw, "total": total, "note": note}

    #AI feedback
    ai_feedback = None
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            history = load_scores()

            history_text = ""
            if history:
                rows = [f"  Test '{e['test']}': Total={e['total']}, Math={e['math']}, R&W={e['rw']}" +
                        (f", Note: {e['note']}" if e.get('note') else "")
                        for e in history[-6:]]
                history_text = "Previous tests (up to last 6):\n" + "\n".join(rows) + "\n\n"

            prompt = (
                f"{history_text}"
                f"New test just logged — '{test}': Total={total}, Math={math}, R&W={rw}."
                + (f" Student note: \"{note}\"." if note else "") +
                "\n\nYou are a concise SAT coach. In 3-4 sentences give actionable feedback: "
                "identify the weaker section, note any trends vs past tests, and suggest one specific study focus. "
                "Be encouraging but direct. Do not repeat the scores back verbatim."
            )

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=180,
                temperature=0.7,
            )
            ai_feedback = resp.choices[0].message.content.strip()
        except Exception as e:
            ai_feedback = None  # silently skip if key is wrong etc.

    entry["ai_feedback"] = ai_feedback

    data = load_scores()
    data.append(entry)
    save_scores(data)

    return jsonify({"success": True, "entry": entry})

@app.route("/api/scores/<int:idx>", methods=["DELETE"])
def delete_score(idx):
    data = load_scores()
    if idx < 0 or idx >= len(data):
        return jsonify({"error": "Invalid index."}), 404
    data.pop(idx)
    save_scores(data)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
