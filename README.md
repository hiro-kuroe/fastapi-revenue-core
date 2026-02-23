# FastAPI Revenue Core

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

## ⚠️ Philosophy

Revenue is not a feature.
It is infrastructure.

This project demonstrates how subscription logic, authentication, and payment verification should align structurally.
