# FastAPI Revenue Core
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Stripe](https://img.shields.io/badge/Stripe-635BFF?style=flat&logo=stripe&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

Production-ready Subscription & Monetization Engine built with FastAPI, Stripe and Docker.

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

## 💳 Demo Flow

1. FREE user hits protected endpoint → `403`
2. Stripe Checkout session completes
3. Webhook verified
4. Subscription state updates (FREE → PRO)
5. Same endpoint → `200`

---

## 🧱 Core Stack

- FastAPI
- Stripe API (Test Mode)
- PostgreSQL
- Docker

---

## 🏗 Architecture

Detailed architecture diagram will be added as implementation progresses.

The goal is structural alignment between:

- Authentication layer
- Subscription state
- Stripe webhook verification
- Revenue logic
- Database consistency

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

### Why This Structure

This architecture separates:

- Authentication logic
- Subscription authorization
- Payment event processing
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

## ⚠️ Philosophy

Revenue is not a feature.
It is infrastructure.

This project demonstrates how subscription logic, authentication, and payment verification should align structurally.
