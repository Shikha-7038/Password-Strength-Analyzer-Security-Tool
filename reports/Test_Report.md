# Test Report - Password Strength Analyzer

## Summary
| Item | Value |
|---|---|
| Automated tests | 34 |
| Result in build environment | 34 passed, 0 failed (run with a stand-in runner; pytest was unavailable there) |
| Your run | Run `python -m pytest -q` and record the result below |
| Data used | Synthetic passwords only |

Your pytest result: `_____ passed, _____ failed`  Date: `_______`

## Functional Test Cases

| ID | Scenario | Input (synthetic) | Expected | Actual (build run) | Test | Status |
|---|---|---|---|---|---|---|
| T01 | Empty input | `""` | Score 0, no crash | 0, VERY WEAK | `test_empty` | Pass |
| T02 | Single character | `a` | VERY WEAK | 20, VERY WEAK | `test_one_char` | Pass |
| T03 | Short numeric | `123456` | VERY WEAK | 0, VERY WEAK | `test_short_numeric` | Pass |
| T04 | Common password | `letmein` | Common-password warning | 0, finding shown | `test_common_message` | Pass |
| T05 | Long repeated | `aaaaaaaaaaaaaaaa` | Score <= 40 | 17, VERY WEAK | `test_long_repeated` | Pass |
| T06 | Lowercase only | `zebraplumtrain` | 1 character type | 1 type | `test_lower_only` | Pass |
| T07 | Uppercase only | `KJHGFDSAPOI` | 1 character type | 1 type | `test_upper_only` | Pass |
| T08 | Numbers only | `90817263` | 1 character type | 1 type, 40 WEAK | `test_numbers_only` | Pass |
| T09 | Symbols only | `!@#$%^&*` | 1 character type | 1 type, 40 WEAK | `test_symbols_only` | Pass |
| T10 | Mixed types | `aB3$xY9!` | 4 types | 4 types | `test_mixed` | Pass |
| T11 | Ascending sequence | `xx1234yy` | Ascending detected | Detected | `test_seq_asc` | Pass |
| T12 | Descending sequence | `9876` | Descending detected | Detected | `test_seq_desc` | Pass |
| T13 | Letter sequence | `abcd` | Detected | Detected | `test_seq_letters` | Pass |
| T14 | Keyboard walk | `myqwerty` | `qwer` detected | Detected | `test_keyboard` | Pass |
| T15 | Repeated characters | `AAAAAA123!` | 1 repeated run | 1 | `test_repeat_chars` | Pass |
| T16 | Repeated substring | `abcabcabc` | 1 repeated block | 1 | `test_repeat_sub` | Pass |
| T17 | Word + number | `welcome123` | Common base word | Detected | `test_word_number` | Pass |
| T18 | Word + year | `admin2026` | Year-like detected | Detected | `test_word_year` | Pass |
| T19 | Personal name | `Rahul@123` + name Rahul | Personal-info finding | Detected | `test_name` | Pass |
| T20 | Birth year | `x1999y` + year 1999 | `birth_year` match | Matched | `test_birth_year` | Pass |
| T21 | Long passphrase | 5 random words | Score >= 61 | 87, VERY STRONG | `test_passphrase_strong` | Pass |
| T22 | Unicode | `пароль-密码-xK9` | No crash | 92, length 13 | `test_unicode` | Pass |
| T23 | Spaces | `correct horse battery` | >= 2 types | Met | `test_spaces` | Pass |
| T24 | Maximum length | 300 x 'x' | Length <= 256 | Truncated to 256 | `test_max_length` | Pass |
| T25 | Score boundaries | 0, 20, 21, 40, 41, 60, 61, 80, 81, 100 | Correct class per band | Correct | `test_boundaries` | Pass |
| T26 | Suggestion generation | `abcd1234` | Sequence advice; password never echoed | Met | `test_suggestions_specific`, `test_password_not_echoed` | Pass |
| T27 | Secure generation | 20 characters | Length 20, score >= 61 | Met (about 99) | `test_generator` | Pass |
| T28 | Password not stored | Record then inspect DB file | Password bytes absent; no password column | Absent | `test_api_privacy` | Pass |
| T29 | Password not logged | Analyze with log capture | Password absent from logs | See note | `test_api_privacy` | Pass* |
| T30 | Analytics storage | Record then GET stats | Total > 0, metadata only | Met | `test_api_privacy` | Pass |

\* The log-capture assertion is only fully exercised by real pytest (it provides the `caplog` fixture). Re-run with pytest to confirm.

## Additional Tests
| Test | Result |
|---|---|
| Policy fails on short password (`test_policy`) | Pass |
| Hashing demo verifies correct and rejects wrong password (`test_hashing`) | Pass |
| `Password123!` not rated above MODERATE (`test_password123_not_strong`) | Pass (score 39) |
| `qwerty2026!` rated WEAK or lower (`test_qwerty_year`) | Pass (score 18) |
| Common-password check (`test_common`) | Pass |

## Manual Checklist (record your own results)
| Check | Pass / Fail | Notes |
|---|---|---|
| Password field masked by default | | |
| Show/Hide toggle works | | |
| Meter and score update while typing | | |
| Four pages load and navigation works | | |
| Dashboard charts render (internet needed for Chart.js CDN) | | |
| No `localStorage` / `sessionStorage` entries | | |
| Request is POST with no password in URL | | |
| Layout usable on a narrow/mobile width | | |

## Known Observations
- Lowercase combinations of ordinary words (e.g. `zebraplumtrain`, score 81) can score higher than a real attacker model would justify because the word list is small.
- Entropy numbers are optimistic for human-made passwords (`Password123!` shows about 72 bits).
