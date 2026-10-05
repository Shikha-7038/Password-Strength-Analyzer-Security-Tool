"""Analytics store: safe aggregate metadata ONLY. There is deliberately no password (or hash) column."""
import sqlite3, random
from pathlib import Path
DB = Path(__file__).resolve().parent / "analytics.db"

def conn():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

def init():
    with conn() as c:
        c.executescript("""CREATE TABLE IF NOT EXISTS analyses(analysis_id INTEGER PRIMARY KEY AUTOINCREMENT, score INTEGER, classification TEXT,
        password_length INTEGER, unique_character_ratio REAL, weakness_count INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS findings(finding_id INTEGER PRIMARY KEY AUTOINCREMENT, analysis_id INTEGER REFERENCES analyses(analysis_id),
        finding_type TEXT, severity TEXT, description TEXT);""")
        if c.execute("SELECT COUNT(*) FROM analyses").fetchone()[0] == 0:
            seed(c)

def record_with(c, res):
    m = res["metrics"]
    cur = c.execute("INSERT INTO analyses(score,classification,password_length,unique_character_ratio,weakness_count) VALUES(?,?,?,?,?)",
                    (res["score"], res["classification"], m["length"], m["unique_character_ratio"], m["weakness_count"]))
    c.executemany("INSERT INTO findings(analysis_id,finding_type,severity,description) VALUES(?,?,?,?)",
                  [(cur.lastrowid, f["type"], f["severity"], f["description"]) for f in res["findings"] if f["severity"] != "good"])

def record(res):
    with conn() as c: record_with(c, res)

def seed(c):
    """Synthetic demo passwords are analyzed then discarded; only metadata is kept."""
    from services.password_analyzer import analyze_password
    from services.password_generator import generate_password, generate_passphrase
    rnd = random.Random(7)  # demo seeding only, not security-sensitive
    bases = ["password", "welcome", "admin", "qwerty", "summer", "dragon", "hello", "letmein"]
    samples = ["123456", "12345678", "aaaaaaaa", "abcd1234", "qwerty2026!"]
    for _ in range(260):
        k = rnd.random()
        if k < .25: s = rnd.choice(bases) + str(rnd.choice([1, 12, 123, 2024, 2026])) + rnd.choice(["", "!", "@"])
        elif k < .4: s = rnd.choice(samples)
        elif k < .6: s = "".join(rnd.choice("abcdefghijklmnop") for _ in range(rnd.randint(6, 11)))
        elif k < .8: s = generate_password(rnd.choice([12, 16, 20, 24]))
        else: s = generate_passphrase(rnd.choice([4, 5, 6]))
        record_with(c, analyze_password(s))

def stats():
    with conn() as c:
        tot, avg = c.execute("SELECT COUNT(*), COALESCE(AVG(score),0) FROM analyses").fetchone()
        cls = {r[0]: r[1] for r in c.execute("SELECT classification, COUNT(*) FROM analyses GROUP BY classification")}
        scores = [r[0] for r in c.execute("SELECT score FROM analyses")]
        lens = [r[0] for r in c.execute("SELECT password_length FROM analyses")]
        weak = [{"type": r[0], "count": r[1]} for r in c.execute("SELECT finding_type, COUNT(*) FROM findings WHERE finding_type NOT IN ('length') GROUP BY finding_type ORDER BY 2 DESC")]
    sh = [sum(1 for s in scores if lo <= s < lo + 10 or (lo == 90 and s == 100)) for lo in range(0, 100, 10)]
    lb = [("<8", lambda n: n < 8), ("8-11", lambda n: 8 <= n < 12), ("12-15", lambda n: 12 <= n < 16), ("16-19", lambda n: 16 <= n < 20), ("20+", lambda n: n >= 20)]
    return {"total": tot, "average_score": round(avg, 1), "classes": {k: cls.get(k, 0) for k in ["VERY WEAK", "WEAK", "MODERATE", "STRONG", "VERY STRONG"]},
            "score_distribution": sh, "length_distribution": {k: sum(1 for n in lens if f(n)) for k, f in lb}, "weaknesses": weak}

def recent(n=10):
    with conn() as c:
        return [dict(r) for r in c.execute("SELECT analysis_id, created_at, score, classification, password_length, weakness_count FROM analyses ORDER BY analysis_id DESC LIMIT ?", (n,))]
