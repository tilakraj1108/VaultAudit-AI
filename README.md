# VaultAudit AI 🔒⚡

> **Zero-Knowledge Local AI Invoice, Receipt & Expense Sorter for Freelancers**  
> *Built with open-weight **Llama 3.2 (3B)** running 100% locally via Ollama.*

---

## 📖 Overview

**VaultAudit AI** is a privacy-first financial intake and tax classification tool built for freelancers, contractors, and boutique agencies. It parses invoices, messy receipts, and billing notifications into structured, tax-deductible expense entries — completely offline, with **zero cloud dependencies** and **zero recurring costs**.

---

## 🎯 The Side-Hustle Problem & Value Proposition

Freelancers face a persistent dilemma during tax season and client expense billing:
1. **Privacy & NDA Risks:** Uploading confidential invoices (which include client names, hourly billing rates, bank wire details, and proprietary project descriptions) to third-party cloud AI vendors risks violating client agreements.
2. **Costly SaaS Subscriptions:** Paying $15–$50/month for cloud expense tracking apps or per-token API fees quickly eats into freelance margins.
3. **Internet Dependency:** Traveling freelancers or consultants working in secure client sites often have restricted or no internet connectivity.

### The Monetization Opportunity
- **One-time purchase desktop tool ($29 - $49):** Solopreneurs love one-time licenses that replace recurring SaaS bills.
- **Agency / CPA bulk pack ($149):** Accounting consultancies can bundle VaultAudit for clients who require HIPAA, SOC2, or NDA compliance.

---

## 🌟 Why Open Innovation Matters Here

- **100% On-Device & Zero-Knowledge:** All inference happens locally via Ollama. No telemetry, no logs, and no data packets leave your laptop.
- **Runs with Zero Internet:** Audits invoices and sorts receipts seamlessly on flights, trains, or in offline secure zones.
- **$0 Running Costs:** With open weights, processing 10,000 documents costs the exact same as processing one: **$0.00**.
- **Model Flexibility & Adaptability:** Effortlessly swap between local open-weight models (`llama3.2:3b`, `llama3.2:1b`, `mistral`, `qwen2.5`) or adjust extraction schemas to support international tax frameworks (US IRS Section 179, EU VAT, Canadian GST).

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│               VaultAudit Web UI (Browser)              │
│    • Modern Dark Glassmorphism Design System           │
│    • Drag & Drop Intake + Sample Invoice Selector      │
│    • Interactive Local Storage Expense Ledger          │
│    • One-Click CSV Accounting Export (TurboTax/Excel)  │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP (Port 5173)
                            ▼
┌────────────────────────────────────────────────────────┐
│             Local Zero-Knowledge Bridge                │
│                     `server.py`                        │
│    • Standard Python HTTP server (zero extra pip deps) │
│    • Strict JSON formatting & prompt engineering       │
│    • Resilient local fallback engine                   │
└───────────────────────────┬────────────────────────────┘
                            │ REST API (Port 11434)
                            ▼
┌────────────────────────────────────────────────────────┐
│                  Ollama Local Engine                   │
│               `llama3.2:3b` (Open Weights)             │
│    • 3.2B parameters, 4-bit quantization (~2.0 GB RAM) │
│    • Strict JSON schema generation & audit notes       │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### Prerequisites
1. **Python 3.8+**
2. **Ollama** installed with the `llama3.2:3b` model:
   ```bash
   ollama pull llama3.2:3b
   ```

### Running the App
1. Clone or navigate into the repository:
   ```bash
   cd "c:\My project AG"
   ```
2. Start the local server:
   ```bash
   python server.py
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```

---

## ✨ Features

- **Instant Samples for Quick Testing:**
  - ☁️ **Cloud Hosting Bill (AWS):** Tests multi-line cloud infrastructure itemization and sales tax extraction.
  - 🚗 **Rideshare Travel Receipt (Uber):** Tests business trip validation and transit deductibility.
  - 💻 **Subcontractor Dev Invoice:** Tests contractor hourly breakdown, ACH wire payment info, and tax IDs.
  - 🖥️ **Office Hardware (Apple / B&H):** Tests Section 179 capital depreciation equipment tagging.
- **Custom Text & File Intake:** Drop any text receipt or paste raw OCR text.
- **Tax Deductibility Tagging:** Automatically classifies expenses into IRS/tax categories (SaaS, Hardware, Travel, Contractor) with reasoned audit explanations.
- **Local Expense Ledger:** Persists all reviewed receipts in browser storage with instant calculation of total deductible expenses.
- **Accountant-Ready CSV Export:** Download clean CSV files ready to hand over to a CPA or import into QuickBooks / Excel.

---

## 🔒 Privacy Guarantee

VaultAudit does not contain external tracking, analytics scripts, or remote network calls. All styling and scripts are served directly from the local Python web server.
