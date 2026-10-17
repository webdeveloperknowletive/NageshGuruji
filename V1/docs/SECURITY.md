# Security Architecture & Threat Model

This document outlines the security controls, threat mitigations, authorization mechanisms, and operational procedures implemented across the Astroveda storefront and JAPAM backend.

---

## 1. Threat Model & Mitigations

| Threat Category | Potential Attack Vector | Implemented Mitigation |
| :--- | :--- | :--- |
| **Insecure Direct Object Reference (IDOR)** | Attacker guesses order number (e.g., `#ORD-001`) and views customer phone, address, and purchase records. | **High-entropy Access Tokens:** Each checkout creates a 256-bit URL-safe token (`secrets.token_urlsafe(32)`). Endpoint `GET /api/v1/orders/<order_number>` strictly requires `X-Order-Token: <token>` or admin Bearer JWT. Guessing order numbers yields HTTP 403. |
| **Untrusted Client Pricing** | User tampers with client-side JavaScript or HTTP payload to checkout a ₹21,000 Rudraksha for ₹1. | **Server-Side Authoritative Pricing:** The browser payload contains *only* `{ product_id, quantity }`. The Flask backend retrieves prices directly from PostgreSQL, recomputes discounts, GST, and shipping, completely ignoring client-submitted amounts. |
| **Inventory Overselling & Concurrency** | Multiple users purchase the last available sacred bead simultaneously. | **Row-Level Database Locking:** During checkout execution, `SELECT ... FOR UPDATE` locks product rows within a single SQL transaction. Stock is atomically verified and decremented before transaction commit. |
| **Duplicate Checkout Replay** | User rapidly clicks "Place Order" or network retry causes duplicate payment/orders. | **Idempotency Keys:** Unique `Idempotency-Key` headers are persisted in the `Order` table. Replays return the existing created order with HTTP 200 without creating duplicate database records or re-decrementing inventory. |
| **Forged Payment Webhooks** | Attacker sends fake `payment.captured` POST to mark an unpaid order as paid. | **HMAC-SHA256 & Fail-Closed Validation:** Every webhook requires a valid `X-Razorpay-Signature` verified with constant-time `hmac.compare_digest`. If `PAYMENT_WEBHOOK_SECRET` is unset, the system refuses the request (`500`). Gateway amounts in paise are verified against the order total. |
| **Replay Attacks on Webhooks** | Attacker replays valid captured webhook payload multiple times. | **Redis Deduplication:** Handled event IDs are tracked in Redis (`wh:event:<id>`) with a 24-hour TTL. Duplicate events return HTTP 200 without duplicate state transitions. |
| **Cross-Origin Resource Sharing (CORS)** | Malicious third-party websites attempt to make authenticated requests from user browsers. | **Strict Origin Allowlist:** Flask `CORS` is restricted to exact environment-configured frontend origins (`CORS_ORIGINS`). Wildcard `*` is strictly disallowed in production. |
| **Credential & Secret Leakage** | Hardcoded API keys, JWT secrets, or DB passwords committed to Git. | **Environment Strictness & .gitignore:** All `.env` files, sqlite DBs, and certificates are excluded via `.gitignore` and `.dockerignore`. Startup validates required variables and terminates immediately if secrets are missing. |

---

## 2. Authentication & Authorization Controls

### Administrative Control Plane
- **Session & JWT Protection:** Admin routes (`/admin/*`) require administrative sessions protected by Flask-Login and Argon2/PBKDF2-SHA256 password hashes.
- **RBAC (Role-Based Access Control):** Permissions are partitioned by role:
  - `superadmin`: System configuration, user management, audit review.
  - `admin`: Inventory, products, orders, pujas, consultations.
  - `support`: Read-only order tracking and consultation status updates.
- **Audit Logging:** Administrative actions (price modifications, stock adjustments, order status cancellations) generate non-repudiable entries in the `audit_logs` table.

### Customer Storefront Access
- **Zero-Trust Client Access:** Customers do not require passwords to buy items (frictionless Vedic checkout). Ownership of order details is strictly granted via the secret order access token stored in the customer's browser `localStorage`.

---

## 3. Input Validation & Defense in Depth

1. **SQL Injection Defense:** All database queries utilize SQLAlchemy 2.0 parameterized queries and ORM objects. Raw string concatenation in SQL is prohibited.
2. **Cross-Site Scripting (XSS):**
   - React 19 / Next.js auto-escapes string content in JSX.
   - Jinja2 templates in Flask use autoescaping enabled by default.
3. **Pincode & Phone Validation:** Phone numbers require E.164 or 10-digit Indian mobile formats (`+91` or `[6-9][0-9]{9}`). Pincodes require 6 numerical digits.
4. **Quantity Bounds:** Quantities are strictly coerced and validated (`1 <= quantity <= available_stock`). Zero, negative, or non-numeric values trigger HTTP 400.

---

## 4. Secret Rotation Procedures

When rotating secrets in production:

1. **`SECRET_KEY` & `JWT_SECRET_KEY`:**
   - Generate a 64-character cryptographic token: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Update `SECRET_KEY` in Coolify backend environment variables.
   - Trigger a rolling restart. (Existing active sessions will be required to re-authenticate).
2. **`PAYMENT_WEBHOOK_SECRET`:**
   - Generate a new webhook secret in Razorpay Dashboard -> Settings -> Webhooks.
   - Update `PAYMENT_WEBHOOK_SECRET` in Coolify backend variables.
   - Save and redeploy backend container before saving the new secret in Razorpay.
3. **Database Credentials (`DATABASE_URL`):**
   - Update PostgreSQL password in PostgreSQL container.
   - Update `DATABASE_URL` in backend container and redeploy.
