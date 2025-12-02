import base64
import pyotp


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed (64-char hex)
    """

    # 1. Convert hex string -> bytes
    seed_bytes = bytes.fromhex(hex_seed)

    # 2. Convert bytes -> base32 string
    seed_b32 = base64.b32encode(seed_bytes).decode("utf-8")

    # 3. Create TOTP object (SHA1, 6 digits, 30s default)
    totp = pyotp.TOTP(seed_b32)

    # 4. Generate current TOTP code
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with ±1 window (default)
    """

    # Convert hex -> bytes
    seed_bytes = bytes.fromhex(hex_seed)

    # Convert bytes -> base32
    seed_b32 = base64.b32encode(seed_bytes).decode("utf-8")

    # Create TOTP object
    totp = pyotp.TOTP(seed_b32)

    # Verify with tolerance window
    return totp.verify(code, valid_window=valid_window)


if __name__ == "__main__":
    # Load seed from data/seed.txt
    with open("data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    print("Current TOTP Code:", code)
