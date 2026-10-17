# Testing & Quality Assurance Guide

This document describes the automated test suites, end-to-end validation procedures, and QA verification checklist for the integrated spiritual commerce platform.

---

## 1. Automated Test Suites

### A. JAPAM Backend (Pytest)

The backend test suite verifies core business rules, database transactions, order calculation, RBAC, IDOR protection, and webhook signature verification.

```powershell
cd "d:\nageshguruji\V1\JAPAM - Copy"
pytest -v
```

#### Test Suite Breakdown (32 Passed Tests):
1. **Catalog & Categories (`tests/test_api_v1.py`):**
   - Products listing and category slug filtering.
   - Single product lookup by slug.
   - Inactive/unpublished product exclusion.
2. **Pricing & Cart Calculation (`tests/test_integration.py`):**
   - Server-side tax calculation (3% Vedic goods GST).
   - Free shipping threshold logic (> ₹999).
   - Dynamic coupon code validation and discount computation.
3. **Atomic Checkout & Idempotency (`tests/test_integration.py`):**
   - Safe order number generation (`#ORD-YYMMDDHHMM-XXXX`).
   - Cryptographic `access_token` issuance (256-bit URL-safe).
   - Deduplication via `idempotency_key` (replays return HTTP 200 without duplicate rows).
   - Inventory decrements using `with_for_update()` row-locking.
4. **IDOR & Security Controls (`tests/test_integration.py`):**
   - Order tracking access requires matching `access_token` or admin JWT.
   - Guessing order numbers without tokens returns `403 Forbidden`.
5. **Payment Webhook & Fail-Closed Integrity (`tests/test_api_v1.py`):**
   - Constant-time HMAC-SHA256 signature verification.
   - Fail-closed behavior (HTTP 500) if webhook secret is missing.
   - Redis-backed event deduplication for 24 hours.
   - Exact amount in paise validation against order total.
6. **Vedic Ritual & Jyotish Bookings (`tests/test_api_v1.py`):**
   - Puja reservation and Sankalp data validation.
   - Kundali consultation submission and reference ID generation.

---

### B. Astroveda Frontend (ESLint & Next.js Production Build)

The frontend test suite verifies TypeScript/JavaScript correctness, zero React 19 hook violations, and production compile optimization.

```powershell
cd "d:\nageshguruji\V1\astroveda"

# 1. Run ESLint checks
npm run lint

# 2. Run Next.js production build
npm run build
```

**Verification Results:**
- ESLint: **0 errors, 0 warnings**.
- Next.js 16.4.2 Turbopack: Successfully compiled 4 static routes (`/`, `/_not-found`), 1 dynamic route (`/products/[slug]`), and optimized SSR chunks without runtime exceptions.

---

## 2. End-to-End Verification Runbook

Follow these 8 steps to verify the entire platform interactively:

1. **Start Services:** Launch backend and frontend development servers.
2. **Verify Health:** Open `http://localhost:5000/api/v1/health` in browser or curl (verifies `{"status":"healthy"}`).
3. **Storefront Visual Inspection:** Open `http://localhost:3000`. Confirm all sacred visuals (gold accents, Marathi typography, Devanagari headings, product cards, puja sections, Jyotish consultation) render smoothly without visual regressions.
4. **Authoritative Cart Addition:** Add a "1 Mukhi Rudraksha" and "Navagraha Yantra" to the cart. Observe the cart sidebar accurately displaying server-reconciled prices and counts.
5. **Vedic Checkout Flow:**
   - Click "ऑर्डर करा / Checkout".
   - Confirm the checkout modal opens with billing fields.
   - Enter name, email, phone, and address.
   - Select "Cash on Delivery" or "Online Payment (Razorpay)".
   - Click "ऑर्डर निश्चित करा / Confirm Order".
   - Verify modal transitions to Order Confirmed state displaying real order number `#ORD-YYMMDD...`.
6. **Admin Verification:**
   - Log into `http://localhost:5000/admin` using `admin@japam.local` / `AdminPassword123!`.
   - Navigate to "Orders" table.
   - Verify the newly created order appears with exact matching items, totals, customer details, and `pending_payment` / `cod` status.
7. **Puja & Jyotish Verification:**
   - Open Puja section on storefront, click "पूजा बुक करा", enter devotee Sankalp and submit. Confirm booking ID returned.
   - Navigate to Jyotish section, submit birth date and time, confirm consultation reference ID returned.
   - Verify both entries appear in JAPAM Admin under Bookings and Consultations.
8. **IDOR & Security Boundary:**
   - Attempt `GET /api/v1/orders/<order_number>` without `X-Order-Token` header.
   - Confirm server returns `403 Forbidden` (`{"error": "Unauthorized access to this order"}`).
