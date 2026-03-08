# FastAPI Revenue Core
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Stripe](https://img.shields.io/badge/Stripe-635BFF?style=flat&logo=stripe&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

Production-ready FastAPI backend for subscription-based SaaS products.

Includes working Stripe Checkout, verified Webhook processing,
time-based access control, and automatic expiration handling.

---

## 🚀 What This Is

FastAPI Revenue Core is a production-oriented backend foundation for SaaS products that need:

- JWT authentication (access + refresh)
- Role-based access control
- Subscription state management (FREE / PRO / CANCELED / EXPIRED)
- Stripe Checkout integration
- Webhook signature verification
- Idempotent event handling
- Docker-ready deployment

This repository focuses on real-world monetization flows — not tutorials.

---

## Need help with Stripe or FastAPI?

If you are experiencing issues with:

- Stripe webhook
- subscription state sync
- Stripe Checkout integration

please submit the incident intake form below.

👉 **[Stripe / FastAPI Incident Intake Form](./Intake.md)**  

You can also contact me directly:  

📧 fastapienne@gmail.com

---

## 🔍 Verified Runtime Behavior

FREE user → GET /stripe/pro-content → 403

After successful Stripe Checkout:  
- Webhook (invoice.payment_succeeded) received  
- DB updated: FREE → PRO  
- GET /stripe/pro-content → 200

When current_period_end <= now:  
- GET /stripe/pro-content → 403  
- Access denied by subscription guard

---

## 🧱 Core Stack

- FastAPI
- Stripe API (Test Mode)
- SQLAlchemy
- SQLite
- Docker

---

## 🧠 Structural Design (Implemented)

Layer 1: Authentication (JWT)  
Layer 2: Subscription Guard (service-level enforcement)  
Layer 3: Stripe Event Processing (Webhook + Idempotency)  
Layer 4: Database State Engine (time-based truth source)

Each layer is isolated and testable.

---

### High-Level Flow

```text
Client
  ↓
FastAPI (Auth Layer - JWT)
    ↓
    Subscription Guard (FREE / PRO check)
      ↓
      Stripe Checkout
        ↓
        Stripe Webhook
          ↓
          Subscription State Update (DB)
  ↓
Protected Endpoint returns 200

```

---

## 🔄 Subscription State Engine (Implemented)

The subscription engine is time-based.

### States (Database)
- FREE
- PRO
- CANCELED
- EXPIRED

### Truth Source

Access control is determined by:

current_period_end > now

Status alone does not grant access.

### Automatic Expiration

When a user with PRO or CANCELED reaches the expiration date:

- Access returns 403
- Access is denied when current_period_end <= now.
  The expiration rule is enforced at the API guard layer.

This ensures database state and runtime authorization remain aligned.

```

## 🔄 Subscription State Transition

```text
                grant
   FREE  ─────────────────▶  PRO
                               │
                               │ cancel
                               ▼
                           CANCELED
                               │
                               │ expiration reached
                               ▼
                            EXPIRED

```

Expiration rule:  
If current_period_end <= now  
→ Access returns 403  
→ subscription_status is updated to EXPIRED

---

### Why This Structure

This architecture separates:

- Authentication logic
- Subscription authorization
- Stripe event processing
- Database state transitions

Each layer can fail independently — and must be verifiable independently.

This separation prevents revenue logic from leaking into transport logic.

---

## Scope

This repository does NOT include:

- Frontend implementation
- Billing UI
- Stripe production configuration
- Infrastructure provisioning (Terraform, etc.)

It focuses strictly on backend revenue architecture.

---

## 🔧 Operational Readiness

Designed to prevent:

- Subscription state drift
- Time-zone based access bugs
- Webhook replay issues
- Authorization inconsistencies

Revenue logic must fail safely.
This repository enforces that principle.

---

## ⚠️ Philosophy

Revenue is not a feature.
It is infrastructure.

This project demonstrates how subscription logic, authentication, and payment verification should align structurally.

---

This repository is intended for engineers who need a structurally sound subscription backend foundation — not a tutorial.

It is built to be read, inspected, and adapted for production systems.

---

## ⚙️ Run Locally

```bash
git clone https://github.com/hiro-kuroe/fastapi-revenue-core

cd fastapi-revenue-core

pip install -r requirements.txt

uvicorn app.main:app --reload
```

