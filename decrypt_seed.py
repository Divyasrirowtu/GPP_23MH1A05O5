import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_seed_b64, private_key):
    # Fix base64 padding
    missing_padding = len(encrypted_seed_b64) % 4
    if missing_padding != 0:
        encrypted_seed_b64 += '=' * (4 - missing_padding)
    
    ciphertext = base64.b64decode(encrypted_seed_b64)
    
    # RSA decryption
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')

