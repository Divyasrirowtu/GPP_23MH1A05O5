import os
import base64
import hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from generate_totp import generate_totp_code, verify_totp_code
import time

app = FastAPI()


# ---------------------------------------
# Helper: Load RSA Private Key
# ---------------------------------------
def load_private_key():
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)



# ---------------------------------------
# Helper: Decrypt Seed
# ---------------------------------------
def decrypt_seed_internal(encrypted_seed_b64: str) -> str:
    private_key = load_private_key()

    ciphertext = base64.b64decode(encrypted_seed_b64)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    hex_seed = plaintext.decode()

    # Validate 64 hex chars
    if len(hex_seed) != 64:
        raise ValueError("Invalid seed length")

    if not all(c in "0123456789abcdef" for c in hex_seed):
        raise ValueError("Seed must be lowercase hex only")

    return hex_seed


# ---------------------------------------
# Models
# ---------------------------------------
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


# ---------------------------------------
# POST /decrypt-seed
# ---------------------------------------
@app.post("/decrypt-seed")
def decrypt_seed(req: DecryptSeedRequest):
    try:
        hex_seed = decrypt_seed_internal(req.encrypted_seed)

        os.makedirs("data", exist_ok=True)
        with open("data/seed.txt", "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(500, f"Decryption failed: {str(e)}")


# ---------------------------------------
# GET /generate-2fa
# ---------------------------------------
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists("data/seed.txt"):
        raise HTTPException(500, "Seed not decrypted yet")

    with open("data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    valid_for = 30 - (int(time.time()) % 30)

    return {"code": code, "valid_for": valid_for}


# ---------------------------------------
# POST /verify-2fa
# ---------------------------------------
@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(400, "Missing code")

    if not os.path.exists("data/seed.txt"):
        raise HTTPException(500, "Seed not decrypted yet")

    with open("data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    result = verify_totp_code(hex_seed, req.code)

    return {"valid": result}
