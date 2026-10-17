# Astroveda + JAPAM Spiritual Commerce Platform

> **Production-grade spiritual commerce, Vedic rituals, and astrology platform integrating Astroveda Next.js 16 storefront with JAPAM Flask backend and admin panel.**

---

## 1. System Overview

This platform integrates two specialized systems into a unified, secure commerce ecosystem:

- **Astroveda Storefront (`/astroveda`):**
  - Next.js 16 (App Router), React 19, CSS modules with Vedic gold & saffron design system.
  - Authentic Marathi & Sanskrit spiritual aesthetics.
  - Sacred items catalog (Rudraksha 1-7 Mukhi, Ratna/Gemstones, Yantras, Malas, Bracelets).
  - Dynamic Vedic Puja booking (Mahamrityunjaya, Navagraha, Rudrabhishek) with devotee Sankalp.
  - Jyotish Kundali consultation requests.
  - Cart, wishlist, and live checkout modal with authoritative server-side price calculation.

- **JAPAM Backend & Admin Control Plane (`/JAPAM - Copy`):**
  - Python Flask application with SQLAlchemy 2.0 and Gunicorn.
  - Authoritative REST API (`/api/v1`) handling pricing, stock concurrency, and order creation.
  - Cryptographically secure order access tokens (IDOR protection).
  - Idempotent checkout transactions with row-level locks (`with_for_update()`).
  - Strict HMAC-SHA256 signature verification and Redis deduplication for payment webhooks.
  - Full-featured administrative control panel with RBAC, inventory, bookings, and audit logs.

- **Infrastructure:**
  - Production-ready for **Hostinger VPS (Ubuntu 24.04)** managed via **Coolify**.
  - PostgreSQL 16 on private network as canonical source of truth.
  - Redis 7 for rate-limiting, caching, and idempotency.
  - Isolated Docker bridge network, persistent volumes, and Traefik reverse proxy with Let's Encrypt SSL.

---

## 2. Architecture & Data Flow

```
[Devotee Browser / Mobile Phone]
             │ (HTTPS: 443)
             ▼
[Coolify / Traefik SSL Termination]
       │                        │
       ▼                        ▼
[Astroveda Storefront]    [JAPAM Backend & Admin]
(Next.js 16 :3000)        (Flask / Gunicorn :5000)
       │                        │
       └─────► REST API v1 ─────┤
                                ├──► [PostgreSQL 16] (Persistent DB)
                                ├──► [Redis 7] (Cache & Locks)
                                └──► [Razorpay / Webhooks]
```

---

## 3. Quickstart (Local Development)

### A. One-Command Setup with Docker Compose
```bash
docker compose up --build -d
docker compose exec backend python seed.py
```
- **Storefront:** [http://localhost:3000](http://localhost:3000)
- **Admin Panel:** [http://localhost:5000/admin](http://localhost:5000/admin) (`admin@japam.local` / `AdminPassword123!`)
- **API Health:** [http://localhost:5000/api/v1/health](http://localhost:5000/api/v1/health)

### B. Standalone Local Setup
1. **Backend:**
   ```powershell
   cd "JAPAM - Copy"
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python seed.py
   python wsgi.py
   ```
2. **Frontend:**
   ```powershell
   cd astroveda
   npm install
   npm run dev
   ```

---

## 4. Verification & Testing

### Automated Test Suites:
```powershell
# 1. Run all 32 Backend Pytests
cd "JAPAM - Copy"
pytest -v

# 2. Run Frontend Lint and Next.js Production Build
cd ../astroveda
npm run lint
npm run build
```
- **Backend Tests:** 32/32 tests passed (Catalog, Cart, Concurrency, Checkout Idempotency, IDOR Protection, Webhook HMAC).
- **Frontend Build:** 0 ESLint errors, 0 warnings, clean Next.js 16 Turbopack production compilation.

---

## 5. Documentation Suite

Detailed architectural, deployment, and security specifications are provided in the `/docs` directory:

| Document | Purpose |
| :--- | :--- |
| **[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)** | Component topology, trust boundaries, and data flows. |
| **[`docs/API_INTEGRATION.md`](docs/API_INTEGRATION.md)** | Full REST API contracts, payloads, query parameters, and error codes. |
| **[`docs/SECURITY.md`](docs/SECURITY.md)** | Threat model, IDOR protection, webhook fail-closed mechanics, and secret rotation. |
| **[`docs/ENVIRONMENT_VARIABLES.md`](docs/ENVIRONMENT_VARIABLES.md)** | Comprehensive checklist of public build-time vs private runtime secrets. |
| **[`docs/LOCAL_DEVELOPMENT.md`](docs/LOCAL_DEVELOPMENT.md)** | Standalone and Docker Compose local setup instructions. |
| **[`docs/COOLIFY_DEPLOYMENT.md`](docs/COOLIFY_DEPLOYMENT.md)** | Hostinger VPS Ubuntu 24.04 step-by-step Coolify deployment guide. |
| **[`docs/BACKUP_RESTORE.md`](docs/BACKUP_RESTORE.md)** | PostgreSQL dumps, upload archiving, and recovery validation runbooks. |
| **[`docs/TESTING.md`](docs/TESTING.md)** | Automated test coverage and end-to-end QA validation procedures. |

---

## 6. Default Administrative Credentials

Seeded automatically via `seed.py`:

- **Superadmin:** `admin@japam.local` | `AdminPassword123!`
- **Store Manager:** `manager@japam.local` | `ManagerPassword123!`
