# Local Development Guide

This guide describes how to run and test both Astroveda (Next.js storefront) and JAPAM (Flask backend & admin) on your local workstation.

---

## 1. Prerequisites

- **Node.js:** v20.x or v22.x+ (Recommended: LTS)
- **Python:** v3.11+
- **Docker & Docker Compose:** (Optional, for unified containerized environment)
- **Git**

---

## 2. Option A: Quickstart with Docker Compose (Recommended)

To spin up the entire platform (Frontend, Backend, PostgreSQL, Redis, Worker) in a production-identical topology:

```bash
# 1. From the repository root (d:\nageshguruji\V1)
docker compose up --build -d

# 2. View streaming logs
docker compose logs -f

# 3. Seed initial products, categories, and admin account
docker compose exec backend python seed.py
```

### Access URLs:
- **Astroveda Storefront:** [http://localhost:3000](http://localhost:3000)
- **JAPAM Admin Dashboard:** [http://localhost:5000/admin](http://localhost:5000/admin)
- **REST API v1:** [http://localhost:5000/api/v1](http://localhost:5000/api/v1)

---

## 3. Option B: Running Standalone (No Docker)

### Step 1: Start JAPAM Backend

```powershell
# Open Terminal 1
cd "d:\nageshguruji\V1\JAPAM - Copy"

# Create and activate virtual environment (if not already done)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run database migrations or seed data
python seed.py

# Start Flask development server on port 5000
python wsgi.py
```

Verify backend is responding:
```powershell
curl http://localhost:5000/api/v1/health
# Output: {"status":"healthy"}
```

### Step 2: Start Astroveda Storefront

```powershell
# Open Terminal 2
cd "d:\nageshguruji\V1\astroveda"

# Install dependencies
npm install

# Start Next.js development server on port 3000
npm run dev
```

The storefront will automatically connect to `http://localhost:5000/api/v1`.

---

## 4. Default Seed Credentials

After executing `python seed.py`, the following administrative accounts are initialized:

- **Superadmin:**
  - Email: `admin@japam.local`
  - Password: `AdminPassword123!`
  - Role: `superadmin`
- **Store Manager:**
  - Email: `manager@japam.local`
  - Password: `ManagerPassword123!`
  - Role: `admin`

---

## 5. Running Automated Tests

### Run Backend Pytest Suite
```powershell
cd "d:\nageshguruji\V1\JAPAM - Copy"
pytest -v
# Output: 32 passed
```

### Run Frontend ESLint and Production Build
```powershell
cd "d:\nageshguruji\V1\astroveda"
npm run lint
npm run build
```
