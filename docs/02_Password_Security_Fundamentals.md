# 02 - Password Security Fundamentals

| Term | Explanation |
|---|---|
| Authentication | Proving who you are (password, MFA, passkey) |
| Authorization | Deciding what you may do after authentication |
| Password | A secret string used to authenticate |
| Password hashing | One-way transformation used to verify a password without storing it |
| Salt | Unique random value added before hashing so identical passwords differ |
| Key stretching | Deliberately slow hashing to make guessing expensive |
| MFA | Two or more factors: know, have, are |
| Password manager | Tool that generates and stores unique passwords |
| Passphrase | Long password made of random words |
| Reuse | Using the same password on multiple services |

## Plaintext vs Hash

| Plaintext storage | Hash storage |
|---|---|
| Database leak exposes every password | Leak exposes only hashes |
| Admins and attackers can read passwords | Original is not directly readable |
| Never acceptable | Standard practice with a proper algorithm |

```
Password -> + Salt -> Password Hashing Function -> Stored Hash
Login: submitted password -> same function + stored salt -> compare
```

## Password-Hashing Functions

| Algorithm | Notes |
|---|---|
| Argon2id | Modern recommended choice; memory-hard |
| bcrypt | Widely supported; adaptive cost |
| scrypt | Memory-hard; used in this project's demo |
| PBKDF2 | Standards-friendly; needs high iteration counts |

- General-purpose fast hashes (MD5, SHA-1, SHA-256 alone) are built for speed, which helps attackers who steal a database.
- Hashing is **not** encryption: hashes are one-way, encryption is reversible with a key.
- `backend/services/hashing_demo.py` shows `hash_password()` and `verify_password()` with a synthetic password only. It is not connected to analyzer input.

## Why Not Even Hash Analyzer Inputs?
- Users may type real passwords. Storing even a hash creates a list of guessable targets and needless privacy risk.
- Analytics need only score, class and length.

## Brute-Force Resistance (Concept Only)
- Longer, less predictable passwords generally increase guessing difficulty.
- Real resistance depends on:

| Factor | Effect |
|---|---|
| Attacker model | Targeted guess vs bulk list |
| Predictability | Common patterns are tried first |
| Hashing algorithm | Slow hashes cost attackers more |
| Work factor | Higher cost per guess |
| Rate limiting | Limits online attempts |
| Online vs offline | Offline attacks on stolen hashes are much faster |

- This tool shows only an "educational estimate", never a guaranteed time-to-crack. It does not crack passwords.

## Modern Policy Principles (NIST SP 800-63B style)
- Favor length; allow spaces and all printable characters.
- Block common and breached passwords.
- Do not require arbitrary composition rules or periodic rotation.
- Rotate when compromise is suspected.
- Encourage password managers and MFA.

## 10 Password Security Rules
| # | Rule | Reason |
|---|---|---|
| 1 | Use unique passwords | Limits credential stuffing |
| 2 | Prefer long passwords/passphrases | Larger search space |
| 3 | Avoid predictable information | Names and years are guessed first |
| 4 | Avoid common passwords | Lists are public |
| 5 | Never reuse | One breach should not open many accounts |
| 6 | Use a password manager | Random, unique, stored safely |
| 7 | Enable MFA | Stops password-only takeover |
| 8 | Never share passwords | Sharing removes accountability |
| 9 | Beware phishing | Strong passwords can still be handed over |
| 10 | Change after compromise | Rotate on evidence, not a calendar |

## Real-World Login Security
| Layer | Role |
|---|---|
| Strong password | Raises guessing cost |
| MFA | Blocks stolen-password logins |
| Secure hashing | Limits damage from database leaks |
| Rate limiting / lockout | Slows online guessing |
| Session security | Protects after login |
| Phishing protection | Stops password theft |
| Monitoring | Detects stuffing and anomalies |

A very strong password alone cannot stop phishing, malware, session theft or reuse across breached sites.
