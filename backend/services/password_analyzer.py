"""Password analysis engine. Everything runs in memory; the password is never stored, logged or returned."""
import math, re
from pathlib import Path

MAX_LEN = 128
COMMON = {l.strip().lower() for l in (Path(__file__).resolve().parents[2] / "data" / "common_passwords.txt").read_text().splitlines() if l.strip()}
BASE_WORDS = {"password", "welcome", "admin", "letmein", "hello", "login", "master", "dragon", "monkey", "sunshine",
              "football", "iloveyou", "summer", "winter", "school", "qwerty", "secret", "princess", "shadow", "test"}
ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]
LEET = str.maketrans("@4310$5!7", "aaeiossit")
BANDS = [(20, "VERY WEAK"), (40, "WEAK"), (60, "MODERATE"), (80, "STRONG"), (100, "VERY STRONG")]  # project-defined, not a standard


def analyze_length(pw, bands=(8, 12, 16)):
    n = len(pw)
    label = "Very short" if n < bands[0] else "Short" if n < bands[1] else "Better length" if n < bands[2] else "Strong length contribution"
    return {"length": n, "label": label}


def analyze_characters(pw):
    kinds = {"lowercase": any(c.islower() for c in pw), "uppercase": any(c.isupper() for c in pw),
             "numbers": any(c.isdigit() for c in pw), "symbols": any(not c.isalnum() and not c.isspace() for c in pw),
             "spaces": any(c.isspace() for c in pw)}
    u = len(set(pw))
    return {"kinds": kinds, "character_type_count": sum(kinds.values()), "unique_character_count": u,
            "unique_character_ratio": round(u / len(pw), 2) if pw else 0}


def is_common_password(pw):
    s = pw.lower()
    return s in COMMON or s.translate(LEET) in COMMON


def detect_sequences(pw, min_run=4):
    s, hits, i = pw.lower(), [], 0
    while i < len(s) - 1:
        d = ord(s[i + 1]) - ord(s[i])
        j = i + 1
        while d in (1, -1) and j < len(s) and ord(s[j]) - ord(s[j - 1]) == d and s[j].isalnum():
            j += 1
        if d in (1, -1) and s[i].isalnum() and j - i >= min_run:
            hits.append("ascending" if d == 1 else "descending")
            i = j
        else:
            i += 1
    return hits


def detect_keyboard_patterns(pw, min_run=4):
    s = pw.lower()
    return sorted({row[i:i + min_run][::step] for row in ROWS for step in (1, -1)
                   for i in range(len(row) - min_run + 1) if row[i:i + min_run][::step] in s})


def detect_repetition(pw):
    chars = [m.group(0) for m in re.finditer(r"(.)\1{3,}", pw)]
    subs = [m.group(0) for m in re.finditer(r"(.{2,4}?)\1{2,}", pw)]
    return {"repeated_chars": len(chars), "repeated_substrings": len(subs)}


def detect_predictable_structure(pw):
    """word + number/symbol patterns such as welcome123, Admin2026, Password123!"""
    low = pw.lower()
    core = re.sub(r"[\d\W_]+$", "", low)            # strip trailing digits/symbols
    tail = low[len(core):]
    known = lambda w: w in BASE_WORDS or w in COMMON
    base = len(core) >= 3 and len(tail) <= 6 and (known(core) or known(core.translate(LEET)))
    year = bool(re.search(r"(19|20)\d{2}", pw))
    contains = [w for w in BASE_WORDS if w in low or w in low.translate(LEET)] if len(pw) < 16 else []
    return {"common_base_word": base, "year_like": year, "dictionary_word": bool(contains)}


def check_context(pw, ctx):
    s, hits = pw.lower(), []
    for key in ("first_name", "organization"):
        v = (ctx.get(key) or "").strip().lower()
        if len(v) >= 3 and v in s:
            hits.append(key)
    y = str(ctx.get("birth_year") or "").strip()
    if len(y) == 4 and y.isdigit() and y in pw:
        hits.append("birth_year")
    return hits


def estimate_theoretical_entropy(pw, effective_len=None):
    """Entropy ~ L x log2(N). Assumes random choice, so it is optimistic for human-made passwords."""
    c = analyze_characters(pw)["kinds"]
    pool = 26 * c["lowercase"] + 26 * c["uppercase"] + 10 * c["numbers"] + 33 * c["symbols"] + c["spaces"]
    return round((effective_len if effective_len is not None else len(pw)) * math.log2(max(pool, 2)), 1)


def classify(score):
    return next(label for cap, label in BANDS if score <= cap)


def generate_suggestions(f):
    s = []
    if f["length"] < 12: s.append("Use at least 12 characters; 16 or more is better. Consider a long passphrase of random words.")
    if f["common"]: s.append("This matches a commonly used password. Choose something unique that is not on public lists.")
    if f["sequences"]: s.append("Your password contains a predictable sequence. Remove runs like 1234 or abcd.")
    if f["keyboard"]: s.append("Avoid keyboard walks such as qwerty or asdf; they are among the first patterns guessed.")
    if f["repetition"]: s.append("Repeated characters or blocks add length but not unpredictability. Replace them with unrelated characters.")
    if f["structure"]: s.append("A common word plus digits or a year is easy to guess. Avoid predictable word-number combinations.")
    if f["context"]: s.append("Avoid including your name, birth year or organization in a password.")
    if f["kinds"] < 3 and f["length"] < 16: s.append("Mix character types, but remember that length and randomness matter more than symbols.")
    s += ["Use a different password for every account to limit credential-stuffing damage.",
          "Use a password manager to generate and store unique passwords.", "Enable MFA wherever it is available."]
    return s


def check_policy(pw, f, minimum_length=12, common_check=True, personal_check=True):
    fails = []
    if len(pw) < minimum_length: fails.append(f"Shorter than {minimum_length} characters")
    if len(pw) > MAX_LEN: fails.append(f"Longer than {MAX_LEN} characters")
    if common_check and f["common"]: fails.append("Common password")
    if personal_check and f["context"]: fails.append("Contains personal information")
    return {"result": "POLICY PASS" if not fails else "POLICY FAIL", "failures": fails}


def analyze_password(password, context=None):
    pw = (password or "")[:MAX_LEN * 2]
    context = context or {}
    if not pw:
        return {"score": 0, "classification": "VERY WEAK", "findings": [], "suggestions": ["Start typing a password to see analysis."],
                "metrics": {"length": 0, "unique_character_ratio": 0, "weakness_count": 0}, "breakdown": {}, "policy": check_policy("", {"common": False, "context": []})}
    L, C = analyze_length(pw), analyze_characters(pw)
    common, seq, kb = is_common_password(pw), detect_sequences(pw), detect_keyboard_patterns(pw)
    rep, st, ctx = detect_repetition(pw), detect_predictable_structure(pw), check_context(pw, context)
    eff_len = len(re.sub(r"(.)\1+", r"\1", pw))  # collapse runs so 'aaaa...' does not earn length credit
    bits = estimate_theoretical_entropy(pw, eff_len)
    is_rep = bool(rep["repeated_chars"] or rep["repeated_substrings"])
    is_struct = st["common_base_word"] or st["dictionary_word"]
    findings = []
    def add(t, sev, d): findings.append({"type": t, "severity": sev, "description": d})
    add("length", "good" if len(pw) >= 12 else "medium", f"{L['label']} ({len(pw)} characters)")
    if C["character_type_count"] >= 3: add("diversity", "good", "Good character variety (helpful, but not decisive)")
    if common: add("common_password", "high", "Your password matches a commonly used password pattern and should not be used.")
    if seq: add("sequence", "medium", f"Predictable {'/'.join(sorted(set(seq)))} sequence detected")
    if kb: add("keyboard_pattern", "medium", "Keyboard-walk pattern detected")
    if is_rep: add("repetition", "medium", "Repeated characters or substrings detected")
    if st["common_base_word"]: add("word_number", "high", "Common word with predictable numbers or symbols")
    elif st["dictionary_word"]: add("dictionary_word", "medium", "Contains a common dictionary word")
    if st["year_like"]: add("year_pattern", "low", "Year-like number detected")
    if ctx: add("personal_info", "high", "Password appears to contain personal information.")
    patterns = sum(bool(x) for x in (seq, kb, is_rep, is_struct, ctx))
    b = {"length": round(min(35, eff_len * 35 / 16), 1), "diversity": round(min(15, C["character_type_count"] * 3.75), 1),
         "unique_ratio": round(C["unique_character_ratio"] * 10, 1), "pattern_resistance": max(0, 20 - 7 * patterns),
         "not_common": 0 if common else 10, "unpredictability": 0 if (patterns or common) else round(min(10, bits / 8), 1)}
    pen = {"common": 40 * common, "keyboard": 10 * bool(kb), "sequence": 10 * bool(seq), "repetition": 12 * is_rep,
           "word_number": 32 * st["common_base_word"] + 8 * (st["dictionary_word"] and not st["common_base_word"]), "personal": 15 * bool(ctx)}
    score = int(max(0, min(100, sum(b.values()) - sum(pen.values()))))
    cap = 20 if len(pw) < 8 else 40 if len(pw) < 10 else 60 if len(pw) < 12 else 100  # short passwords cannot rate higher
    score = min(score, cap)
    f = {"length": len(pw), "common": common, "sequences": seq, "keyboard": kb, "repetition": is_rep,
         "structure": is_struct, "context": ctx, "kinds": C["character_type_count"]}
    resist = "Very low" if bits < 28 else "Low" if bits < 45 else "Medium" if bits < 65 else "High" if bits < 90 else "Very high"
    return {"score": score, "classification": classify(score), "findings": findings, "suggestions": generate_suggestions(f),
            "metrics": {"length": len(pw), "length_label": L["label"], "character_type_count": C["character_type_count"],
                        "unique_character_count": C["unique_character_count"], "unique_character_ratio": C["unique_character_ratio"],
                        "entropy_bits": bits, "guess_resistance": resist + " (educational estimate only)", "pattern_count": patterns,
                        "weakness_count": len([x for x in findings if x["severity"] != "good"])},
            "breakdown": {"points": b, "penalties": {k: v for k, v in pen.items() if v}}, "policy": check_policy(pw, f)}
