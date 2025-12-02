import binascii
import base64
import pyotp

def generate_totp_code(hex_seed: str) -> str:
    seed_bytes = binascii.unhexlify(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode("utf-8")
    totp = pyotp.TOTP(seed_base32, digits=6, interval=30)
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    seed_bytes = binascii.unhexlify(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode("utf-8")
    totp = pyotp.TOTP(seed_base32, digits=6, interval=30)
    return totp.verify(code, valid_window=valid_window)

if __name__ == "__main__":
    with open("data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    print("Current TOTP code:", code)

    valid = verify_totp_code(hex_seed, code)
    print("Is code valid?", valid)
