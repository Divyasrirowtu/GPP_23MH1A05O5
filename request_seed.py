import json
import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id: str, github_repo_url: str):
    # 1. Read student public key
    with open("student_public.pem", "r") as f:
        public_key_pem = f.read()

    # 2. Prepare payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_pem
    }

    # 3. Send POST request
    response = requests.post(
        API_URL,
        json=payload,
        timeout=30
    )

    # 4. Parse response
    data = response.json()

    if data.get("status") != "success":
        print("Error:", data)
        return

    encrypted_seed = data["encrypted_seed"]

    # 5. Save to file
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    print("Encrypted seed saved to encrypted_seed.txt")


if __name__ == "__main__":
    # REPLACE THESE:
    student_id = "YOUR_STUDENT_ID"
    github_repo_url = "https://github.com/yourusername/your-repo-name"

    request_seed(student_id, github_repo_url)
