# PKI-TOTP Authentication Microservice

## Description
This project implements a secure, containerized authentication microservice demonstrating enterprise-grade security practices using **Public Key Infrastructure (PKI)** and **Time-based One-Time Password (TOTP)** two-factor authentication. The service provides cryptographic operations, REST API endpoints, cron-based 2FA logging, and persistent storage in Docker.

---

## Features
- **RSA 4096-bit Encryption**
  - RSA/OAEP with SHA-256 for seed decryption
  - RSA-PSS with SHA-256 for commit signature
- **TOTP 2FA**
  - SHA-1, 30-second period, 6-digit codes
  - ±1 period tolerance for verification
- **REST API Endpoints**
  - `POST /decrypt-seed` — Decrypt encrypted seed and store persistently
  - `GET /generate-2fa` — Generate current TOTP code
  - `POST /verify-2fa` — Verify TOTP code
- **Dockerized**
  - Multi-stage build (builder + runtime)
  - Cron daemon for logging 2FA codes every minute
  - Persistent storage via Docker volumes
  - UTC timezone enforced
- **Commit Proof**
  - Commit hash signed with student private key and encrypted with instructor public key

---

## Technology Stack
- Python 3.11 (FastAPI)
- `pyotp` for TOTP generation
- `cryptography` for RSA operations
- Docker + Docker Compose
- Cron for automated tasks
- REST API for integration

---

## Project Structure
├── app/
│ ├── main.py # API server
│ ├── crypto.py # RSA key generation & encryption/decryption
│ └── totp.py # TOTP generation & verification
├── scripts/
│ └── log_2fa_cron.py # Cron script to log 2FA codes
├── cron/
│ └── 2fa-cron # Cron job configuration
├── student_private.pem # Student private key (committed)
├── student_public.pem # Student public key (committed)
├── instructor_public.pem # Instructor public key (committed)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitattributes
├── .gitignore
└── README.md


---

## Setup Instructions

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd <repo-directory>

2. Build Docker Container
docker-compose build

3. Start Container
docker-compose up -d

4. API Endpoints
Decrypt Seed
curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\": \"$(cat encrypted_seed.txt)\"}"

Generate 2FA Code
curl http://localhost:8080/generate-2fa

Verify 2FA Code
CODE=$(curl -s http://localhost:8080/generate-2fa | jq -r '.code')
curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"$CODE\"}"

Cron Job

Runs every minute (cron/2fa-cron)

Logs TOTP code to /cron/last_code.txt in UTC

Format: YYYY-MM-DD HH:MM:SS - 2FA Code: XXXXXX

Docker Volumes

/data — Persistent storage for decrypted seed

/cron — Logs for cron output

Key Notes

Timezone: UTC for TOTP and cron logs

Private Key: student_private.pem committed for Docker usage (do not reuse elsewhere)

Encrypted Seed: Stored in encrypted_seed.txt (do not commit)

Line Endings: Cron file uses LF (.gitattributes ensures this)