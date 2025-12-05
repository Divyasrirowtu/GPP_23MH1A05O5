import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes


def load_private_key():
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP + SHA-256.
    Returns the 64-character hex seed.
    """

    # 1. Base64 decode
    ciphertext = base64.b64decode(encrypted_seed_b64)

    # 2. RSA OAEP decrypt
    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. Convert bytes → string
    hex_seed = plaintext_bytes.decode("utf-8")

    # 4. Validate seed format
    if len(hex_seed) != 64:
        raise ValueError("Seed must be 64 hex characters!")

    if not all(c in "0123456789abcdef" for c in hex_seed):
        raise ValueError("Seed is not valid lowercase hex!")

    return hex_seed


if __name__ == "__main__":
    # Load encrypted seed
    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()

    private_key = load_private_key()
    seed = decrypt_seed(encrypted_seed_b64, private_key)

    print("Decrypted Seed:", seed)

    # Save to data/seed.txt
    import os
    os.makedirs("data", exist_ok=True)

    with open("data/seed.txt", "w") as f:
        f.write(seed)

    print("Seed saved to data/seed.txt")
