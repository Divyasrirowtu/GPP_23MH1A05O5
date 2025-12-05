import base64
import pyotp


# -------------------------
# Generate TOTP Code
# -------------------------
def generate_totp_code(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    seed_b32 = base64.b32encode(seed_bytes).decode("utf-8")
    totp = pyotp.TOTP(seed_b32, digits=6, interval=30)
    return totp.now()


# -------------------------
# Verify TOTP Code
# -------------------------
def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    seed_bytes = bytes.fromhex(hex_seed)
    seed_b32 = base64.b32encode(seed_bytes).decode("utf-8")
    totp = pyotp.TOTP(seed_b32, digits=6, interval=30)
    return totp.verify(code, valid_window=valid_window)


# Local test (optional)
if __name__ == "__main__":
    with open("data/seed.txt", "r") as f:
        seed = f.read().strip()

    code = generate_totp_code(seed)
    print("Current TOTP:", code)
