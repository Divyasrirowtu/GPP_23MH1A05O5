import subprocess
import base64
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


# -----------------------------
# Step 1: Get latest commit hash
# -----------------------------
def get_commit_hash() -> str:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            capture_output=True,
            text=True,
            check=True
        )
        commit_hash = result.stdout.strip()
        if len(commit_hash) == 40:
            return commit_hash
        else:
            raise ValueError("Invalid commit hash format")
    except Exception as e:
        print("Error: Unable to get commit hash:", e)
        exit(1)


# -------------------------------------------------
# Step 2: Load student private key (PEM, RSA key)
# -------------------------------------------------
def load_private_key(path: str):
    pem_data = Path(path).read_bytes()
    return serialization.load_pem_private_key(
        pem_data,
        password=None,
        backend=default_backend()
    )


# ----------------------------------------------------
# Step 3: Load instructor public key (PEM, RSA key)
# ----------------------------------------------------
def load_public_key(path: str):
    pem_data = Path(path).read_bytes()
    return serialization.load_pem_public_key(
        pem_data,
        backend=default_backend()
    )


# --------------------------------------------------------------
# Step 4: Sign message using RSA-PSS with SHA-256
# --------------------------------------------------------------
def sign_message(message: str, private_key) -> bytes:
    message_bytes = message.encode("utf-8")
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


# ---------------------------------------------------------------------
# Step 5: Encrypt signature using RSA-OAEP with instructor public key
# ---------------------------------------------------------------------
def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


# -----------------------------------------
# Step 6: Main proof generation workflow
# -----------------------------------------
def generate_proof():
    print("\n--- Generating Commit Proof ---\n")

    commit_hash = get_commit_hash()
    print("Commit Hash:", commit_hash)

    # Load keys
    private_key = load_private_key("student_private.pem")
    public_key = load_public_key("instructor_public.pem")

    # Sign commit hash
    signature = sign_message(commit_hash, private_key)
    print("Signature (bytes):", len(signature))

    # Encrypt signature
    encrypted_sig = encrypt_with_public_key(signature, public_key)
    print("Encrypted Signature (bytes):", len(encrypted_sig))

    # Base64 encode
    encrypted_sig_b64 = base64.b64encode(encrypted_sig).decode()

    # Save output
    output = (
        f"Commit Hash: {commit_hash}\n"
        f"Encrypted Signature (Base64):\n{encrypted_sig_b64}\n"
    )

    Path("commit_proof.txt").write_text(output)
    print("\nSaved → commit_proof.txt")
    print("\nDONE ✔")


if __name__ == "__main__":
    generate_proof()
