# API Integration Guide: Astroveda & JAPAM

This document specifies all REST API v1 contracts implemented by the JAPAM backend (`/api/v1`) and consumed by the Astroveda storefront.

---

## 1. Global Specifications

- **Base URL (Production):** `https://api.yourdomain.com/api/v1`
- **Base URL (Local Dev):** `http://localhost:5000/api/v1`
- **Default Content-Type:** `application/json`
- **Error Response Envelope:**
  ```json
  {
    "error": "Error description message",
    "code": "ERROR_CODE_OPTIONAL"
  }
  ```
- **Standard HTTP Codes:**
  - `200 OK`: Request succeeded.
  - `201 Created`: Resource successfully created.
  - `400 Bad Request`: Payload validation failed or insufficient inventory.
  - `401 Unauthorized`: Missing or invalid authentication token.
  - `403 Forbidden`: Authenticated user lacks permission.
  - `404 Not Found`: Resource does not exist.
  - `429 Too Many Requests`: Rate limit threshold exceeded.
  - `500 Internal Server Error`: Server exception (fails closed).

---

## 2. Catalog & Products

### `GET /catalog/products`
Retrieves paginated list of active, published sacred products.

- **Query Parameters:**
  - `category` *(optional, string)*: Filter by category slug (e.g., `rudraksha`, `gemstones`, `yantra`, `mala`).
  - `search` *(optional, string)*: Keyword search across product name and description.
  - `page` *(optional, integer, default: 1)*: Page number.
  - `per_page` *(optional, integer, default: 20)*: Items per page.
- **Response `200 OK`:**
  ```json
  {
    "items": [
      {
        "id": 1,
        "name": "1 Mukhi Rudraksha (Round Nepal)",
        "slug": "1-mukhi-rudraksha",
        "category": { "id": 1, "name": "Rudraksha", "slug": "rudraksha" },
        "price": 21000.0,
        "compare_at_price": 25000.0,
        "sku": "RUD-1M-001",
        "stock": 5,
        "is_active": true,
        "is_featured": true,
        "primary_image": "/static/uploads/rudraksha-1m.jpg",
        "short_description": "Sacred certified round Nepali Ek Mukhi bead."
      }
    ],
    "total": 29,
    "page": 1,
    "pages": 2
  }
  ```

### `GET /catalog/products/<slug>`
Retrieves comprehensive details of a single product.

- **URL Parameter:** `slug` *(string)*: Product slug.
- **Response `200 OK`:**
  ```json
  {
    "id": 1,
    "name": "1 Mukhi Rudraksha (Round Nepal)",
    "slug": "1-mukhi-rudraksha",
    "description": "Full sacred properties, energization details, and laboratory certificate.",
    "price": 21000.0,
    "compare_at_price": 25000.0,
    "stock": 5,
    "sku": "RUD-1M-001",
    "weight_grams": 4.2,
    "dimensions": "22mm",
    "origin": "Nepal",
    "images": [
      { "id": 1, "url": "/static/uploads/rudraksha-1m.jpg", "is_primary": true }
    ],
    "specifications": {
      "ruling_planet": "Sun (Surya)",
      "deity": "Lord Shiva",
      "certification": "IGI Lab Certified"
    }
  }
  ```

### `GET /catalog/categories`
Retrieves all product categories with counts.

- **Response `200 OK`:**
  ```json
  [
    { "id": 1, "name": "Rudraksha", "slug": "rudraksha", "product_count": 12 },
    { "id": 2, "name": "Gemstones (Ratna)", "slug": "gemstones", "product_count": 9 },
    { "id": 3, "name": "Yantra", "slug": "yantra", "product_count": 4 },
    { "id": 4, "name": "Mala & Rosary", "slug": "mala", "product_count": 4 }
  ]
  ```

---

## 3. Cart & Calculations

### `POST /cart/calculate`
Authoritative calculation of subtotal, applicable taxes (3% Vedic Goods GST), shipping rates, coupon discounts, and grand total. **Does not modify database records.**

- **Request Body:**
  ```json
  {
    "items": [
      { "product_id": 1, "quantity": 1 },
      { "product_id": 3, "quantity": 2 }
    ],
    "coupon_code": "VEDA10"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "items": [
      {
        "product_id": 1,
        "name": "1 Mukhi Rudraksha",
        "price": 21000.0,
        "quantity": 1,
        "line_total": 21000.0,
        "in_stock": true,
        "available_stock": 5
      },
      {
        "product_id": 3,
        "name": "3 Mukhi Rudraksha",
        "price": 850.0,
        "quantity": 2,
        "line_total": 1700.0,
        "in_stock": true,
        "available_stock": 25
      }
    ],
    "subtotal": 22700.0,
    "discount": 2270.0,
    "tax": 612.9,
    "shipping": 0.0,
    "total": 21042.9,
    "coupon_applied": {
      "code": "VEDA10",
      "discount_type": "percentage",
      "discount_value": 10
    }
  }
  ```
- **Error Response `400 Bad Request`:**
  ```json
  {
    "error": "Product ID 999 not found or inactive."
  }
  ```

---

## 4. Checkout & Orders

### `POST /orders/checkout`
Atomically validates cart, acquires row-level locks on inventory (`SELECT ... FOR UPDATE`), decrements stock, creates an order, generates a cryptographically secure `access_token`, and returns order metadata.

- **Request Headers:**
  - `Idempotency-Key` *(recommended, string)*: UUID v4 to guarantee deduplication on retry or network disconnect.
- **Request Body:**
  ```json
  {
    "idempotency_key": "c7a9e1d8-4f2b-47e2-a0e1-7d9a1c8f3b2a",
    "customer": {
      "name": "Rohit Joshi",
      "email": "rohit@example.com",
      "phone": "+919876543210"
    },
    "shipping_address": {
      "line1": "Flat 402, Shivshankar Heights",
      "line2": "Prabhat Road, Deccan Gymkhana",
      "city": "Pune",
      "state": "Maharashtra",
      "pincode": "411004",
      "country": "India"
    },
    "items": [
      { "product_id": 1, "quantity": 1 }
    ],
    "coupon_code": "VEDA10",
    "payment_method": "razorpay"
  }
  ```
- **Response `201 Created` (or `200 OK` on idempotent retry):**
  ```json
  {
    "order_number": "#ORD-2610161830-7491",
    "access_token": "q3B8vL7dK0_xM9wP2rT5yZ8aC1eF4gH7jK0mN3pQ6sT",
    "status": "pending_payment",
    "payment_method": "razorpay",
    "subtotal": 21000.0,
    "discount": 2100.0,
    "tax": 567.0,
    "shipping": 0.0,
    "total": 19467.0,
    "created_at": "2026-10-16T18:30:00Z",
    "razorpay_order_id": "order_Hk29fL9kM3j1a"
  }
  ```
- **Error Responses:**
  - `400 Bad Request`: `"Insufficient stock for 1 Mukhi Rudraksha. Available: 0"`
  - `400 Bad Request`: `"Missing required customer details: phone, name"`

### `GET /orders/<order_number>`
Retrieves tracking details and item status. Protected against Insecure Direct Object References (IDOR).

- **Authorization:** Must provide either:
  1. `X-Order-Token` header: `<access_token>`
  2. Query parameter: `?token=<access_token>`
  3. Admin Bearer Token: `Authorization: Bearer <jwt_token>`
- **Response `200 OK`:**
  ```json
  {
    "order_number": "#ORD-2610161830-7491",
    "status": "processing",
    "payment_status": "paid",
    "payment_method": "razorpay",
    "customer": {
      "name": "Rohit Joshi",
      "email": "rohit@example.com"
    },
    "items": [
      {
        "product_id": 1,
        "name": "1 Mukhi Rudraksha",
        "price": 21000.0,
        "quantity": 1
      }
    ],
    "total": 19467.0,
    "tracking_number": "BLUE-DART-8491029",
    "carrier": "Blue Dart Express",
    "created_at": "2026-10-16T18:30:00Z"
  }
  ```
- **Error Response `403 Forbidden`:**
  ```json
  {
    "error": "Unauthorized access to this order. Valid order access token is required."
  }
  ```

---

## 5. Vedic Services & Consultations

### `POST /services/book-puja`
Books an auspicious Vedic ritual (Mahamrityunjaya, Navagraha Shanti, Rudrabhishek).

- **Request Body:**
  ```json
  {
    "puja_name": "Mahamrityunjaya Anushthan",
    "sankalp_name": "Anil Kulkarni",
    "gotra": "Kashyap",
    "kuldevta": "Khanderaya (Jejuri)",
    "preferred_date": "2026-11-04",
    "phone": "+919822011223",
    "email": "anil@example.com",
    "address": "Sadashiv Peth, Pune 411030",
    "special_prayers": "Health, prosperity, and obstacle removal."
  }
  ```
- **Response `201 Created`:**
  ```json
  {
    "booking_id": "PUJA-202611-9482",
    "status": "confirmed",
    "message": "Sankalp successfully registered. Acharya will review your muhurat."
  }
  ```

### `POST /services/request-consultation`
Submits birth chart (Kundali) details for Jyotish consultation.

- **Request Body:**
  ```json
  {
    "name": "Priyanka Deshmukh",
    "birth_date": "1994-08-15",
    "birth_time": "06:45",
    "birth_place": "Kolhapur, Maharashtra",
    "consultation_type": "Kundali & Career Guidance",
    "phone": "+919819001122",
    "email": "priyanka@example.com",
    "query": "Analysis for planetary doshas and gemstone recommendation."
  }
  ```
- **Response `201 Created`:**
  ```json
  {
    "consultation_id": "JYOT-2610-1082",
    "status": "scheduled",
    "message": "Kundali details received. Our Jyotish Acharya will prepare your Patrika."
  }
  ```

---

## 6. Payment Webhook

### `POST /payments/webhook`
Webhook handler for gateway transaction status updates.

- **Headers:**
  - `X-Razorpay-Signature`: HMAC-SHA256 signature calculated over raw request body with `PAYMENT_WEBHOOK_SECRET`.
- **Payload Example:**
  ```json
  {
    "event": "payment.captured",
    "payload": {
      "payment": {
        "entity": {
          "id": "pay_O0k1J2L3m4N5o6",
          "order_id": "order_Hk29fL9kM3j1a",
          "amount": 1946700,
          "currency": "INR",
          "status": "captured",
          "method": "upi"
        }
      }
    }
  }
  ```
- **Security & Idempotency Rules:**
  1. Signature verified using `hmac.compare_digest`.
  2. Missing webhook secret causes immediate `500 Server Error` (fail closed).
  3. Event ID is checked in Redis cache (`wh:event:<id>`); repeated events return `200 OK` without re-processing.
  4. Amount in paise is validated against order total.
  5. Order transitions to `paid` and `processing`.
