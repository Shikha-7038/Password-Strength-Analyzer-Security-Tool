"""EDUCATIONAL ONLY: salted, slow password hashing with stdlib scrypt. Never wired to analyzer input."""
import hashlib, hmac, os

def hash_password(pw, n=2**14):
    salt = os.urandom(16)
    return f"scrypt${n}${salt.hex()}${hashlib.scrypt(pw.encode(), salt=salt, n=n, r=8, p=1).hex()}"

def verify_password(pw, stored):
    _, n, salt, h = stored.split("$")
    cand = hashlib.scrypt(pw.encode(), salt=bytes.fromhex(salt), n=int(n), r=8, p=1).hex()
    return hmac.compare_digest(cand, h)
