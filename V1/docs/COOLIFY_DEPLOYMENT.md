# Coolify Deployment Guide (Hostinger VPS / Ubuntu 24.04)

This guide provides end-to-end instructions for deploying the integrated Astroveda + JAPAM platform onto a Hostinger VPS running Ubuntu 24.04 with Coolify.

---

## 1. Architecture on Coolify

```
[Internet HTTPS Request]
        │
        ▼
[Traefik Proxy (Coolify Managed SSL / Let's Encrypt)]
        ├── store.yourdomain.com ──► astroveda-frontend:3000
        └── api.yourdomain.com   ──► japam-backend:5000
                                           │
                                ┌──────────┴──────────┐
                                ▼                     ▼
                       postgres-db:5432         redis-cache:6379
                       (Private Network)        (Private Network)
```

- **Domain 1 (Customer Storefront):** `https://store.yourdomain.com` (or `https://yourdomain.com`) -> Points to Next.js (port 3000).
- **Domain 2 (API & Admin Control):** `https://api.yourdomain.com` -> Points to Flask (port 5000).
- **Internal Database & Redis:** Isolated on Coolify's internal Docker bridge network; **no external ports exposed**.

---

## 2. Server Preparation (Ubuntu 24.04)

Log in via SSH to your Hostinger VPS:

```bash
# Update Ubuntu packages
sudo apt update && sudo apt upgrade -y

# Verify Docker and Curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Coolify (if not already installed)
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

Once installed, navigate to `http://YOUR_SERVER_IP:8000` to complete the initial Coolify setup.

---

## 3. Provisioning Managed Services in Coolify

### Step A: PostgreSQL 16
1. In Coolify, click **New Resource** -> **Databases** -> **PostgreSQL**.
2. Set resource name to `japam-postgres`.
3. Configure environment parameters:
   - `POSTGRES_DB`: `japam_db`
   - `POSTGRES_USER`: `japam_user`
   - `POSTGRES_PASSWORD`: `GenerateAStrongSecretPassword`
4. Attach persistent volume: `/var/lib/postgresql/data`.
5. Note the internal hostname: `japam-postgres` (Port 5432).

### Step B: Redis 7
1. Click **New Resource** -> **Databases** -> **Redis**.
2. Set resource name to `japam-redis`.
3. Note internal hostname: `japam-redis` (Port 6379).

---

## 4. Deploying JAPAM Backend Service

1. In Coolify, click **New Resource** -> **Application** -> **Git Repository** (or Dockerfile).
2. Point repository path to `JAPAM - Copy` (or your root repository with Dockerfile location `./JAPAM - Copy/Dockerfile`).
3. Set **Port:** `5000`.
4. Set **Domains:** `https://api.yourdomain.com`.
5. Attach Persistent Volume for media uploads:
   - **Host Path:** `/var/coolify/volumes/japam-uploads`
   - **Mount Path:** `/app/uploads`
6. Configure Environment Variables in Coolify UI:
   ```bash
   FLASK_ENV=production
   FLASK_DEBUG=0
   PORT=5000
   SECRET_KEY=<generate_with_python_secrets>
   JWT_SECRET_KEY=<generate_with_python_secrets>
   DATABASE_URL=postgresql+psycopg://japam_user:GenerateAStrongSecretPassword@japam-postgres:5432/japam_db
   REDIS_URL=redis://japam-redis:6379/0
   CORS_ORIGINS=https://store.yourdomain.com,https://yourdomain.com
   PAYMENT_WEBHOOK_SECRET=<your_razorpay_webhook_secret>
   RAZORPAY_KEY_ID=<your_razorpay_key_id>
   RAZORPAY_KEY_SECRET=<your_razorpay_secret>
   ```
7. Configure Post-Deployment Command:
   ```bash
   flask db upgrade || python seed.py
   ```
8. **Health Check:**
   - Path: `/api/v1/health`
   - Interval: 15s
   - Expected Status: 200

Click **Deploy**.

---

## 5. Deploying Astroveda Storefront Service

1. In Coolify, click **New Resource** -> **Application** -> **Git Repository**.
2. Base directory: `./astroveda`.
3. Dockerfile path: `./astroveda/Dockerfile`.
4. Set **Port:** `3000`.
5. Set **Domains:** `https://store.yourdomain.com` (with automatic SSL / Let's Encrypt enabled).
6. Configure Environment Variables:
   > [!IMPORTANT]
   > Make sure `NEXT_PUBLIC_API_BASE_URL` is configured under **Build Pack Variables** or marked as available at build time.
   ```bash
   NODE_ENV=production
   PORT=3000
   NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com/api/v1
   ```
7. **Health Check:**
   - Path: `/`
   - Interval: 15s
   - Expected Status: 200

Click **Deploy**.

---

## 6. Verification Checklist

1. Open `https://store.yourdomain.com` on a mobile device or desktop browser.
2. Verify that sacred items (1-7 Mukhi Rudraksha, Ratna, Yantra) load dynamically.
3. Add a product to cart and click **Checkout**:
   - Verify modal opens with authentic Marathi/Sanskrit styling.
   - Enter test customer details and click **Confirm Order**.
   - Verify order number `#ORD-YYMMDD...` is generated and confirmed.
4. Navigate to `https://api.yourdomain.com/admin`:
   - Log in using seeded credentials (`admin@japam.local`).
   - Confirm new order appears in the administrative dashboard with status `pending_payment` or `cod`.
