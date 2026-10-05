# Password Strength Analyzer & Security Suggestion Tool

Privacy-focused defensive security tool: scores passwords on length, predictability, common-password checks, pattern analysis, entropy concepts and optional personal context, then explains what to fix. Passwords are analyzed in memory and never stored, logged, returned or sent to external services.

## Run
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py        # open http://127.0.0.1:5000
python -m pytest -q          # 34 tests
```
(Charts load Chart.js from a CDN, so the first page load needs internet.)

## Structure
`backend/services/` analyzer, generator (`secrets`), hashing demo (scrypt) · `backend/db.py` metadata-only SQLite (no password column) · `frontend/index.html` live meter + dashboard · `data/common_passwords.txt` small educational list · `tests/` unit + privacy tests.

## API
`POST /api/analyze` `{password, context?, record?}` → score, classification, findings, suggestions, metrics, policy · `POST /api/generate-password` · `GET /api/dashboard/stats` · `GET /api/analytics/weaknesses`

## Scoring (project-defined, not a standard)
Length ≤35, variety ≤15, unique ratio ≤10, pattern resistance ≤20, not-common 10, unpredictability ≤10, minus penalties for common, keyboard, sequence, repetition, word+number and personal info. Bands: 0-20 VERY WEAK, 21-40 WEAK, 41-60 MODERATE, 61-80 STRONG, 81-100 VERY STRONG. Entropy ≈ L × log2(N) assumes random choice and is optimistic for human passwords; guess resistance is an educational estimate only.

## Limitations
Small word lists, no breach-corpus check, heuristic scoring. Not a replacement for MFA, rate limiting and proper hashing. Use synthetic passwords for demos and screenshots.
