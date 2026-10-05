"""Flask API. Passwords are processed in memory only: never logged, stored, echoed or placed in URLs."""
import os, sys, time, logging
from collections import defaultdict, deque
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flask import Flask, jsonify, request, send_from_directory
import db
from services.password_analyzer import analyze_password, MAX_LEN
from services.password_generator import generate_password, generate_passphrase

app = Flask(__name__, static_folder=str(Path(__file__).resolve().parents[1] / "frontend"), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 4096
logging.getLogger("werkzeug").setLevel(logging.WARNING)
LIMIT, hits = int(os.getenv("RATE_LIMIT_PER_MIN", 120)), defaultdict(deque)
db.init()

@app.before_request
def rate_limit():
    q = hits[request.remote_addr]; now = time.time()
    while q and now - q[0] > 60: q.popleft()
    if len(q) >= LIMIT: return jsonify(error="Too many requests"), 429
    q.append(now)

@app.after_request
def headers(r):
    r.headers.update({"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer"})
    return r

@app.errorhandler(Exception)
def fail(e):  # generic message: never echo request content
    code = getattr(e, "code", 500)
    return jsonify(error="Request could not be processed"), (code if isinstance(code, int) else 500)

@app.get("/")
def index(): return send_from_directory(app.static_folder, "index.html")

@app.post("/api/analyze")
def analyze():
    d = request.get_json(silent=True)
    if not isinstance(d, dict) or not isinstance(d.get("password", ""), str): return jsonify(error="Invalid request"), 400
    if len(d["password"]) > MAX_LEN * 2: return jsonify(error="Password too long"), 413
    res = analyze_password(d["password"], d.get("context") if isinstance(d.get("context"), dict) else {})
    if d.get("record") and d["password"]: db.record(res)  # metadata only
    return jsonify(res)

@app.post("/api/generate-password")
def generate():
    d = request.get_json(silent=True) or {}
    if d.get("mode") == "passphrase": return jsonify(password=generate_passphrase(d.get("words", 5)), kind="passphrase")
    return jsonify(password=generate_password(d.get("length", 20), d.get("upper", True), d.get("lower", True), d.get("digits", True), d.get("symbols", True)), kind="password")

@app.get("/api/dashboard/stats")
def stats(): return jsonify(db.stats())

@app.get("/api/analytics/recent")
def recent(): return jsonify(db.recent())

@app.get("/api/analytics/weaknesses")
def weaknesses(): return jsonify(db.stats()["weaknesses"])

if __name__ == "__main__":
    app.run(port=5000, debug=os.getenv("FLASK_DEBUG") == "1")
