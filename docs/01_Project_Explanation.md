# 01 - Project Explanation

## A. Simple Explanation
- A password strength meter that explains **why** a password is weak, not just how strong it looks.
- You type a password; the tool checks it on your own computer and tells you what is predictable and how to fix it.
- It never saves what you type.

## B. Technical Explanation
- A Flask API receives the password in a POST body and passes it to `analyze_password()`.
- Independent detectors run, results are combined into a 0-100 score, a classification and suggestions.
- Only aggregate metadata may be stored (score, class, length, weakness types).

## Workflow
```
User enters password -> local input validation -> analyzer
 -> length | characters | common check | patterns | sequences | repetition | context | entropy
 -> scoring engine -> score -> classification -> suggestions -> dashboard (metadata only)
```

## Key Concepts

| Concept | Meaning |
|---|---|
| Password strength | How hard a password is to guess; depends on length, unpredictability and the attacker's method |
| Why strong passwords matter | Weak passwords enable account takeover and data theft |
| Why length matters | More characters means a larger search space |
| Why predictability matters | Attackers try likely passwords first (`Password123!`) |
| Entropy | Measure of uncertainty; `L x log2(N)` assumes random choice |
| Dictionary weakness | Passwords built from common words or lists |
| Password reuse | Same password on many sites; one breach exposes all |
| Credential stuffing | Automated login attempts using leaked username/password pairs on other sites |
| Composition rules are insufficient | `Password123!` meets all rules yet is predictable |
| Passphrases | Long random-word passwords: memorable and hard to guess |
| MFA | A second factor limits damage even if the password leaks |

## Industry Relevance

| Domain | Use |
|---|---|
| Authentication systems | Strength feedback at sign-up and reset |
| Banking | Reduce account takeover |
| E-commerce | Protect customer accounts and payments |
| Enterprise portals / SSO | Policy enforcement, fewer helpdesk resets |
| Cloud applications | Protect admin consoles |
| IAM | Banned-password lists, NIST-aligned policy |
| Employee security | Awareness training |
| Customer accounts | Just-in-time coaching |
| Password managers | Strength audits, generators |
| Registration forms | Real-time meters |

## Roles and Skills Demonstrated

| Role | Skills shown by this project |
|---|---|
| Cybersecurity Analyst | Understanding weak-password risk, awareness content |
| Application Security Analyst | Secure coding, privacy-by-design, security testing |
| IAM Analyst | Policy checks, NIST/OWASP-aligned thinking, MFA concepts |
| Security Engineer | Defense in depth, hashing concepts, rate limiting |
| SOC Analyst | Credential-stuffing awareness, indicators of weak credentials |
| Secure Software Developer | Modular Python, tests, safe randomness, API design |
