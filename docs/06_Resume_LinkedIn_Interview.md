# 06 - Resume, LinkedIn and Interview Preparation

## Resume Bullets (choose 2-3)
- Built a privacy-focused password strength analyzer in Python/Flask that scores passwords (0-100) using length, pattern detection, common-password checks, entropy concepts and personal-information checks, without storing or logging the password.
- Implemented detection for sequences, keyboard walks, repeated blocks, word+number structures and context overlap, and generated specific security suggestions instead of generic complexity rules.
- Designed a metadata-only SQLite analytics layer and a 4-page dashboard (7 KPIs, 5 charts), plus 34 automated tests including a privacy test confirming passwords are absent from responses, logs and the database.
- Created a `secrets`-based password/passphrase generator and a hashing demonstration (salted scrypt) to explain secure password storage.

## Skills Section

| Category | Skills |
|---|---|
| Security | Password security, authentication, secure coding, privacy by design, security testing, IAM concepts, MFA, hashing/salting |
| Languages / tools | Python, Flask, JavaScript, HTML/CSS, SQLite, Chart.js, pytest, Git/GitHub |
| Concepts | Entropy, credential stuffing, NIST SP 800-63B principles, OWASP ASVS awareness |

## LinkedIn Project Description
Password Strength Analyzer & Security Suggestion Tool is a defensive cybersecurity project that evaluates passwords beyond basic complexity rules. It combines length, unpredictability, common-password checks, pattern detection (sequences, keyboard walks, repetition, word+number) and personal-information checks to produce a score, specific findings and recommendations. Passwords are analyzed in memory and never stored or logged; the dashboard uses only privacy-safe metadata. The project also includes a secure generator, a hashing demonstration and 34 automated tests.

## LinkedIn Post Draft
> Strong password rules are not always strong passwords. `Password123!` passes most complexity checks, yet it is highly predictable.
> I built a Password Strength Analyzer that evaluates length, predictability, common patterns and personal-information overlap, explains *why* a password is weak, and never stores what you type.
> Built with Python and Flask, with a dashboard, a secure generator and 34 automated tests, including privacy checks.
> Lesson learned: good security tooling must protect the very data it analyzes.
> #CyberSecurity #ApplicationSecurity #PasswordSecurity #Python #SecureCoding

## Interview Questions and Answers

### 1. Explain your project.
I built a privacy-focused password analyzer that scores a password from 0-100 and explains the result. Instead of only checking character types, it combines length, common-password matching, sequences, keyboard patterns, repetition, word+number structures, personal-information overlap and an entropy-style estimate. It returns findings and specific suggestions. The password is processed in memory and never stored, logged or returned; the dashboard only holds metadata like score and length.

### 2. How does your tool decide a password is strong?
It adds points for effective length, variety, unique characters and pattern resistance, then subtracts penalties for common passwords, keyboard walks, sequences, repetition, word+number structures and personal information. Short passwords are capped. The result maps to five classes. Length and unpredictability matter more than symbol count.

### 3. What is entropy, and why is it not enough?
Entropy measures uncertainty; I estimate it as `L x log2(N)`. That assumes each character is chosen randomly, but people choose patterns. `Password123!` gets about 72 bits by that formula yet is very guessable. So I treat entropy as one signal and combine it with pattern and common-password checks.

### 4. Why can `Password123!` be weak even though it meets complexity rules?
It has uppercase, lowercase, number and symbol, but it is a common word plus a predictable number and symbol. Attackers try such mutations early. My tool scores it WEAK (39) while the policy check says PASS, which shows compliance is not strength.

### 5. What is the difference between hashing and encryption?
Hashing is one-way: you can verify a password but not recover it. Encryption is reversible with a key. Systems should store password hashes, not encrypted or plaintext passwords.

### 6. What is salting and why is it used?
A salt is a unique random value added before hashing. It makes identical passwords produce different hashes and defeats precomputed tables, so one cracked hash does not expose every user with the same password.

### 7. Why is a fast hash like plain SHA-256 a poor choice for passwords?
Fast hashes let attackers test enormous numbers of guesses per second after a database leak. Password-hashing functions like Argon2id, bcrypt, scrypt and PBKDF2 are deliberately slow (and some memory-hard), raising the cost per guess.

### 8. How did you protect user privacy in the tool?
The password is sent in a POST body, never in the URL; the API never returns it; request bodies are not logged and errors are generic; the database has no password or hash column; the frontend does not use localStorage or sessionStorage; and a test checks that the password is absent from the response, logs and database file.

### 9. Is a strong password enough to secure an account?
No. Phishing, malware, session theft and password reuse can bypass a strong password. Defense in depth needs MFA, secure hashing, rate limiting, monitoring and user awareness.

### 10. How would you improve the project?
Use a stronger estimator and larger wordlists, add privacy-preserving breach checks (k-anonymity), make policies configurable, add passkey/MFA education, split the analyzer into separate modules, and add accessibility and localization. I would also be explicit that my word list is small, so some lowercase word combinations score higher than a real attacker model would allow.

## Quick Facts

| Fact | Value |
|---|---|
| Automated tests | 34 |
| API endpoints | 5 |
| Frontend pages | 4 |
| Dashboard | 7 KPIs, 5 charts, recent table |
| Score bands | 0-20, 21-40, 41-60, 61-80, 81-100 |
| Policy default | Min 12, max 128 characters |
