# 04 - Security and Privacy Testing

| # | Check | Why it matters | How to verify | Type |
|---|---|---|---|---|
| 1 | Password not stored | A leaked DB must not contain secrets | `test_api_privacy`: password bytes not in the `.db` file | Automated |
| 2 | Password not in logs | Logs are widely accessible and retained | `test_api_privacy` with log capture; review console output | Automated |
| 3 | Password not in database schema | Prevents accidental future storage | Schema check: no `password` column; view DB in SQLite viewer | Automated |
| 4 | Password not returned by API | Responses can be cached or intercepted | `test_api_privacy`: password absent from response; `test_password_not_echoed` | Automated |
| 5 | Password not in URL | URLs end up in history and server logs | DevTools > Network: request is POST, body only | Manual |
| 6 | Password field type | Prevents shoulder surfing | Inspect element: `type="password"` by default | Manual |
| 7 | No unnecessary frontend persistence | Browser storage is readable by scripts | `grep -rn "localStorage\|sessionStorage" frontend` returns nothing | Manual |
| 8 | localStorage empty of secrets | Confirms #7 at runtime | DevTools > Application > Local Storage | Manual |
| 9 | sessionStorage empty of secrets | Same as above | DevTools > Application > Session Storage | Manual |
| 10 | Analytics holds only metadata | Dashboard must never reveal passwords | Inspect `analyses` and `findings` tables | Manual + automated |

## Extra Checks
| Check | Expected |
|---|---|
| Send 300+ characters | 413 or truncation; no crash |
| Send non-JSON body | 400, generic error |
| Send > 120 requests in a minute | 429 |
| Trigger an error | Message does not contain the password |

## Known Gaps
- No CSRF/CORS configuration (same-origin app, no cookies/sessions).
- No authentication on dashboard endpoints (demo project).
- Plain HTTP in development; deploy behind HTTPS.
