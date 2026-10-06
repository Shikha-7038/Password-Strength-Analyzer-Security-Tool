# 03 - Architecture and API

## Folder Structure and Purpose

| Path | Purpose |
|---|---|
| `backend/app.py` | Flask app: routes, rate limiting, security headers, generic error handler |
| `backend/db.py` | SQLite metadata store, synthetic seeding, aggregate queries |
| `backend/services/password_analyzer.py` | Length, character, common, sequence, keyboard, repetition, structure, context, entropy, scoring, suggestions, policy |
| `backend/services/password_generator.py` | Secure generator using `secrets` |
| `backend/services/hashing_demo.py` | Educational salted scrypt hashing (synthetic only) |
| `frontend/index.html` | Analyzer page |
| `frontend/dashboard.html` | Dashboard page |
| `frontend/generator.html` | Generator page |
| `frontend/learn.html` | Education page |
| `frontend/css/style.css` | Shared styling, light/dark theme |
| `frontend/js/*.js` | Shared helpers + one script per page |
| `data/common_passwords.txt` | Small educational common-password list |
| `tests/` | Automated unit and privacy tests |
| `docs/` | Documentation (this folder) |
| `reports/` | Project report and test report |
| `screenshots/` | Proof images (synthetic data only) |
| `requirements.txt`, `.env.example`, `.gitignore` | Dependencies, config template, ignored files |

> Note: the original plan listed separate files (`pattern_detector.py`, `entropy_estimator.py`, `scoring_engine.py`, `suggestion_engine.py`). They are currently functions inside `password_analyzer.py`; splitting them is listed under future work.

## Analyzer Functions

| Function | Responsibility |
|---|---|
| `analyze_length()` | Length and band label |
| `analyze_characters()` | Types, unique count, unique ratio |
| `is_common_password()` | Local list check (with simple leetspeak normalization) |
| `detect_sequences()` | Ascending/descending runs of 4+ |
| `detect_keyboard_patterns()` | Keyboard-row runs of 4+, forward and reverse |
| `detect_repetition()` | Repeated characters and substrings |
| `detect_predictable_structure()` | Word + number, year, dictionary word |
| `check_context()` | Name, birth year, organization overlap |
| `estimate_theoretical_entropy()` | `L x log2(N)` on effective length |
| `generate_suggestions()` | Specific advice, never containing the password |
| `check_policy()` | POLICY PASS / FAIL |
| `analyze_password()` | Orchestrates everything and returns the result |

## Database Schema (metadata only)

**ANALYSES**
| Column | Type |
|---|---|
| analysis_id | INTEGER PK |
| score | INTEGER |
| classification | TEXT |
| password_length | INTEGER |
| unique_character_ratio | REAL |
| weakness_count | INTEGER |
| created_at | TEXT (default CURRENT_TIMESTAMP) |

**FINDINGS**
| Column | Type |
|---|---|
| finding_id | INTEGER PK |
| analysis_id | INTEGER FK |
| finding_type | TEXT |
| severity | TEXT |
| description | TEXT |

There is **no password column and no hash column**. Reasons: a database that never contains passwords cannot leak them, and hashes of user-typed passwords still create privacy risk with no analytics benefit.

## REST API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze` | Analyze a password |
| POST | `/api/generate-password` | Generate password or passphrase |
| GET | `/api/dashboard/stats` | Totals, class counts, score/length distributions, weaknesses |
| GET | `/api/analytics/weaknesses` | Weakness counts |
| GET | `/api/analytics/recent` | Last 10 analyses (metadata) |

### POST /api/analyze
Request:
```json
{ "password": "<processed transiently>", "context": {"first_name": "", "birth_year": "", "organization": ""}, "record": false }
```
- `record: true` stores only metadata (score, class, length, ratio, weakness count, finding types).

Response (shortened):
```json
{ "score": 39, "classification": "WEAK",
  "findings": [{"type": "word_number", "severity": "high", "description": "Common word with predictable numbers or symbols"}],
  "suggestions": ["A common word plus digits or a year is easy to guess. ..."],
  "metrics": {"length": 12, "entropy_bits": 72.3},
  "policy": {"result": "POLICY PASS", "failures": []} }
```

### POST /api/generate-password
| Body | Result |
|---|---|
| `{"length":20,"upper":true,"lower":true,"digits":true,"symbols":true}` | Random password (length clamped 12-64) |
| `{"mode":"passphrase","words":5}` | Passphrase of 4-8 words |

## Validation, Errors, Limits

| Topic | Implementation |
|---|---|
| Validation | JSON object required; `password` must be a string; max 256 characters; request body max 4096 bytes |
| Errors | Generic JSON messages, never echoing request content |
| Status codes | 200, 400, 413, 429, 500 |
| Rate limiting | In-memory sliding window, 120 requests/min per IP (configurable); production should use a shared store or gateway |
| Headers | `Cache-Control: no-store`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer` |
| Transport | **HTTPS is required in production**; the dev server is plain HTTP on localhost |
| Logging | No request-body logging; Werkzeug access logs at WARNING |

## Technology Options

| Option | Stack | Pros | Cons |
|---|---|---|---|
| A (used) | HTML/CSS/JS + Flask + SQLite + Chart.js | Simple, fast to learn, easy demo | Less structured for large UIs |
| B | React + FastAPI + SQLite/PostgreSQL | Modern, typed, auto API docs | More setup, steeper for beginners |

Recommended for a student: **Option A**, then migrate to B as an extension.
