import sys, json, logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from services.password_analyzer import *
from services.password_generator import generate_password, generate_passphrase
from services.hashing_demo import hash_password, verify_password

A = analyze_password
def test_empty(): assert A("")["score"] == 0
def test_one_char(): assert A("a")["classification"] == "VERY WEAK"
def test_short_numeric(): assert A("123456")["classification"] == "VERY WEAK"
def test_common(): assert is_common_password("password123") and not is_common_password("velvet-galaxy")
def test_common_message(): assert any("commonly used" in f["description"] for f in A("letmein")["findings"])
def test_long_repeated(): assert A("aaaaaaaaaaaaaaaa")["score"] <= 40
def test_lower_only(): assert A("zebraplumtrain")["metrics"]["character_type_count"] == 1
def test_upper_only(): assert A("KJHGFDSAPOI")["metrics"]["character_type_count"] == 1
def test_numbers_only(): assert A("90817263")["metrics"]["character_type_count"] == 1
def test_symbols_only(): assert A("!@#$%^&*")["metrics"]["character_type_count"] == 1
def test_mixed(): assert A("aB3$xY9!")["metrics"]["character_type_count"] == 4
def test_seq_asc(): assert "ascending" in detect_sequences("xx1234yy")
def test_seq_desc(): assert "descending" in detect_sequences("9876")
def test_seq_letters(): assert detect_sequences("abcd")
def test_keyboard(): assert "qwer" in detect_keyboard_patterns("myqwerty")
def test_repeat_chars(): assert detect_repetition("AAAAAA123!")["repeated_chars"] == 1
def test_repeat_sub(): assert detect_repetition("abcabcabc")["repeated_substrings"] == 1
def test_word_number(): assert detect_predictable_structure("welcome123")["common_base_word"]
def test_word_year(): assert detect_predictable_structure("admin2026")["year_like"]
def test_name(): assert any(f["type"] == "personal_info" for f in A("Rahul@123", {"first_name": "Rahul"})["findings"])
def test_birth_year(): assert check_context("x1999y", {"birth_year": "1999"}) == ["birth_year"]
def test_passphrase_strong(): assert A("velvet-galaxy-harbor-orchid-saffron")["score"] >= 61
def test_unicode(): assert A("пароль-密码-xK9")["metrics"]["length"] > 5
def test_spaces(): assert A("correct horse battery")["metrics"]["character_type_count"] >= 2
def test_max_length(): assert A("x" * 300)["metrics"]["length"] <= 256
def test_boundaries():
    assert [classify(s) for s in (0, 20, 21, 40, 41, 60, 61, 80, 81, 100)] == ["VERY WEAK"] * 2 + ["WEAK"] * 2 + ["MODERATE"] * 2 + ["STRONG"] * 2 + ["VERY STRONG"] * 2
def test_password123_not_strong(): assert A("Password123!")["score"] <= 60
def test_qwerty_year(): assert A("qwerty2026!")["score"] <= 40
def test_password_not_echoed():
    pw = "Zebra!Unique#9Plum"; assert pw not in json.dumps(A(pw))
def test_suggestions_specific(): assert any("sequence" in s for s in A("abcd1234")["suggestions"])
def test_generator():
    p = generate_password(20); assert len(p) == 20 and A(p)["score"] >= 61
    assert generate_passphrase(5).count("-") == 4
def test_policy(): assert A("short")["policy"]["result"] == "POLICY FAIL"
def test_hashing():
    h = hash_password("demo-pass"); assert verify_password("demo-pass", h) and not verify_password("x", h)
def test_api_privacy(tmp_path, caplog, monkeypatch):
    import db; monkeypatch.setattr(db, "DB", tmp_path / "t.db"); db.init()
    import app as appmod; c = appmod.app.test_client(); pw = "Synthetic#Pw-7391-Plum"
    with caplog.at_level(logging.DEBUG):
        r = c.post("/api/analyze", json={"password": pw, "record": True})
    assert r.status_code == 200 and pw not in r.get_data(as_text=True) and pw not in caplog.text
    assert pw.encode() not in (tmp_path / "t.db").read_bytes()
    assert "password" not in [x[1] for x in db.conn().execute("PRAGMA table_info(analyses)")]
    assert c.get("/api/dashboard/stats").get_json()["total"] > 0
