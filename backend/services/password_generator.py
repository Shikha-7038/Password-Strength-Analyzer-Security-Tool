"""Secure generator. Uses `secrets` (OS CSPRNG), not `random`, which is predictable. Output is never stored."""
import secrets, string

WORDS = ["river", "candle", "photon", "saffron", "galaxy", "orchid", "drift", "ember", "velvet", "harbor", "turtle", "prairie",
         "lantern", "marble", "quartz", "willow", "cobalt", "meadow", "falcon", "thistle", "pepper", "granite", "breeze", "anchor"]

def generate_password(length=20, upper=True, lower=True, digits=True, symbols=True):
    length = max(12, min(64, int(length)))
    pools = [p for on, p in ((upper, string.ascii_uppercase), (lower, string.ascii_lowercase), (digits, string.digits), (symbols, "!@#$%^&*()-_=+[]{}:;,.?")) if on] or [string.ascii_lowercase]
    chars = [secrets.choice(p) for p in pools]  # guarantee one of each selected type
    chars += [secrets.choice("".join(pools)) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

def generate_passphrase(words=5, sep="-"):
    return sep.join(secrets.choice(WORDS) for _ in range(max(4, min(8, int(words)))))
