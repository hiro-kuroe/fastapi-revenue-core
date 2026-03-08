# Stripe / FastAPI Incident Intake

## Stripe / FastAPI Incident Diagnosis Request

This form is used to report issues related to **Stripe payment integration or subscription systems**.

Typical problems include:

- Stripe webhook not triggering
- Subscription status not updating
- Checkout succeeds but user access does not change
- Cancelled subscription still has access

After reviewing the submitted information,  
I will respond with **diagnosis availability and next steps**.

---

## 1. What type of issue are you experiencing?

- [ ] Stripe Checkout
- [ ] Stripe Webhook
- [ ] Subscription state
- [ ] Payment logic
- [ ] API authentication
- [ ] Other

---

## 2. What is happening?

Example:

Webhook is not firing  
Subscription state does not update  
User remains FREE after payment  
Subscription cancellation not reflected

**Description**


Describe the issue here


---

## 3. Backend framework

- [ ] FastAPI
- [ ] Django
- [ ] Node.js
- [ ] Laravel
- [ ] Other

---

## 4. Database

- [ ] PostgreSQL
- [ ] MySQL
- [ ] SQLite
- [ ] Not sure

---

## 5. Stripe mode

- [ ] Test mode
- [ ] Live mode

---

## 6. Related webhook events

Example:


checkout.session.completed
customer.subscription.created
invoice.payment_succeeded


---

## 7. Error message

Paste the error log or upload a screenshot.

Example:


Webhook signature verification failed


---

## 8. Relevant code

If possible, provide:

- Checkout session creation code
- Webhook handler code

GitHub repository link is also acceptable.


Paste code or repository link


---

## 9. Urgency

- [ ] Urgent (within 24 hours)
- [ ] This week
- [ ] Not urgent

---

## 10. What kind of help do you need?

- [ ] Root cause diagnosis only
- [ ] Bug fix / implementation support
- [ ] Not sure yet

---

## 11. Contact information

Email / Discord / Slack


Contact info


---

## Confirmation Message

Thank you for your submission.

I will review the information and reply with  
**diagnosis availability and next steps**.

Additional logs or code snippets may be requested.