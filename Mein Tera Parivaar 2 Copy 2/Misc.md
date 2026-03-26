Perfect 👍
**Receiver user flow ab complete ho gaya hai.**
Main ab **sirf lock + clearly document** kar raha hoon — koi code, koi jump nahi.

---

# 🔒 RECEIVER FLOW – FINAL (LOCKED)

## 🎯 Scope

Receiver ko ek jagah pe:

* current requests ka status
* past requests ka history
  clear dikhni chahiye.

---

## 🧭 FINAL RECEIVER USER FLOW (Phase-1)

### 1️⃣ Item List

* User approved & available items browse karta hai

---

### 2️⃣ Item Detail Page

Yahin se request ka decision hota hai.

#### 🔎 Pre-Request Eligibility Checks (MANDATORY):

System ye sab check karega:

1. User logged-in hai
2. User **approved** hai
3. User ne **minimum 2 approved & active items donate kiye hain**
4. User ke **active requests < 5**
5. Same item ke liye **active requests < 2**
6. Item ki **available quantity > 0**

❌ Agar koi bhi fail:

* “Request Item” button disabled
* Reason clearly visible (UX message)

---

### 3️⃣ Request Create

Sirf jab saare checks pass ho jaayen:

* User quantity select karta hai
* Request create hoti hai
* Default status = `pending`

---

### 4️⃣ My Requests Page

Receiver ko **Active + Past requests dono** dikhenge.

---

## 📄 “My Requests” PAGE – FINAL BEHAVIOUR

### 🔹 Data shown per request:

* Item name
* Requested quantity
* Approved quantity (if accepted)
* Status:

  * pending
  * accepted
  * rejected
  * completed
* Request date

---

### 🔹 Active Requests

**Active =**

* `pending`
* `accepted`

Behaviour:

* Read-only
* Receiver koi action nahi karega
* Sirf wait / status check

---

### 🔹 Past Requests

**Past =**

* `rejected`
* `completed`

Behaviour:

* Read-only history
* No retry button (cooldown rule system handle karega)

---

## 🔒 SYSTEM ENFORCEMENT (important)

* Receiver **kabhi** request ka status change nahi kar sakta
* Eligibility checks backend enforce karega
* UI sirf state + reason dikhayegi

---

## ✅ RECEIVER FLOW STATUS

* Receiver rules ✅
* Eligibility checks ✅
* Request creation flow ✅
* My Requests (Active + Past) ✅

👉 **Receiver user flow PHASE-1 ke liye COMPLETE & LOCKED**

---

## 🧭 Next logical step (tum choose karo)

Ab naturally do options bachte hain:

**A️⃣** Donor user flow define karein
**B️⃣** Receiver flow ka DB → View mapping shuru karein (implementation planning)

Bas reply me **A / B** likho.
