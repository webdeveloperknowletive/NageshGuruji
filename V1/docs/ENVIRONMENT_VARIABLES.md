# Environment Variables Specification

This document details every environment variable required across the Astroveda storefront, JAPAM backend, and database infrastructure.

---

## 1. Summary of Scopes & Sensitivity

| Service | Variable Name | Scope | Sensitivity | Purpose / Description |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend** | `NEXT_PUBLIC_API_BASE_URL` | Build-time & Runtime | Public | Base URL for REST API calls from customer browser |
| **Frontend** | `PORT` | Container Runtime | Non-sensitive | Port on which Next.js server listens (default: `3000`) |
| **Frontend** | `NODE_ENV` | Build-time & Runtime | Non-sensitive | Set to `production` |
| **Backend** | `FLASK_ENV` | Container Runtime | Non-sensitive | Application runtime mode (`production` or `development`) |
| **Backend** | `SECRET_KEY` | Container Runtime | **Secret** | Flask session signing and CSRF protection |
| **Backend** | `JWT_SECRET_KEY` | Container Runtime | **Secret** | Signing key for administrative JWT tokens |
| **Backend** | `DATABASE_URL` | Container Runtime | **Secret** | Connection string for PostgreSQL database |
| **Backend** | `REDIS_URL` | Container Runtime | **Secret** | Connection string for Redis instance (caching, rate limit) |
| **Backend** | `CORS_ORIGINS` | Container Runtime | Non-sensitive | Comma-separated list of allowed frontend origins |
| **Backend** | `PORT` | Container Runtime | Non-sensitive | Gunicorn binding port (default: `5000`) |
| **Backend** | `PAYMENT_WEBHOOK_SECRET` | Container Runtime | **Secret** | Gateway HMAC webhook signature secret |
| **Backend** | `RAZORPAY_KEY_ID` | Container Runtime | Public/Semi | Razorpay merchant key ID |
| **Backend** | `RAZORPAY_KEY_SECRET` | Container Runtime | **Secret** | Razorpay merchant API secret |
| **PostgreSQL**| `POSTGRES_USER` | Container Runtime | Non-sensitive | Superuser name for database |
| **PostgreSQL**| `POSTGRES_PASSWORD` | Container Runtime | **Secret** | Password for database user |
| **PostgreSQL**| `POSTGRES_DB` | Container Runtime | Non-sensitive | Name of default commerce database |

---

## 2. Frontend Configuration (`astroveda/.env.production`)

> [!IMPORTANT]
> `NEXT_PUBLIC_API_BASE_URL` is baked into client-side JS bundles during Next.js compilation. In Coolify, ensure this variable is set in the application build configuration before initiating deployment.

```bash
# Public Base URL pointing to deployed JAPAM REST API v1
NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com/api/v1

# Container Internal Port
PORT=3000

# Environment Mode
NODE_ENV=production
```

---

## 3. Backend Configuration (`JAPAM - Copy/.env`)

```bash
# Flask Environment
FLASK_ENV=production
FLASK_DEBUG=0

# Application Secrets (Must be 64-char random hex in production)
SECRET_KEY=generate_with_python_secrets_token_hex_32
JWT_SECRET_KEY=generate_with_python_secrets_token_hex_32

# Production Database (PostgreSQL)
# Format: postgresql+psycopg://username:password@internal-host:5432/dbname
DATABASE_URL=postgresql+psycopg://japam_user:ChangeThisPostgresPassword@japam-postgres:5432/japam_db

# Redis Cache & Task Broker
# Format: redis://internal-host:6379/0
REDIS_URL=redis://japam-redis:6379/0

# Strict CORS Allowlist (Comma-separated, no trailing slashes)
CORS_ORIGINS=https://store.yourdomain.com,https://yourdomain.com

# Server Bindings
PORT=5000
GUNICORN_WORKERS=4
GUNICORN_THREADS=2

# Payment Gateway Configuration
RAZORPAY_KEY_ID=rzp_test_placeholder_key_id
RAZORPAY_KEY_SECRET=placeholder_secret_key
PAYMENT_WEBHOOK_SECRET=placeholder_webhook_secret

# Upload Directory
UPLOAD_FOLDER=/app/uploads
MAX_CONTENT_LENGTH=10485760 # 10 MB in bytes
```

---

## 4. Generating Cryptographic Secrets

Run this one-liner in Python to generate cryptographically secure keys:

```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32)); print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```
