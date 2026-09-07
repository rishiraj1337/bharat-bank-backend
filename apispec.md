# Bharat Bank Omnichannel Platform — API Specification & Architecture

## Overview
The Bharat Bank Omnichannel Banking Platform consists of two detached, independently deployable backend servers:

1. **Core Banking System (CBS) / FLEXCUBE & OBDX Mock Server** (`:8000`)
   - Serving canonical CBS integration contracts (v1, v2, v3) in XML/JSON envelopes.
   - Swagger UI: `http://localhost:8000/docs`
2. **Omnichannel Digital Banking Backend** (`:8080`)
   - Serving customer-facing and backoffice experiences with custom multi-collection Swagger UI dropdown.
   - **Collection 1:** Flutter Mobile Banking Application (Retail & Corporate)
   - **Collection 2:** React Admin Console & Backoffice Operations Portal
   - Swagger UI: `http://localhost:8080/docs`

---

## 🚀 Running Both Servers with Docker
To build and spin up both microservices with a single docker command:

```bash
docker compose up --build
```
Or in detached mode:
```bash
docker compose up -d
```

### Local Execution (Without Docker):
```bash
./run_all.sh
```

---

## 📱 Collection 1: Flutter Mobile App API Endpoints (`/api/v1/app`)

### 1. System, Versioning & Theming
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/app/version` | App version, min supported version, force update, and downstream subsystems health. |
| `GET` | `/api/v1/app/theme` | Dynamic theme configuration with light/dark palettes (3 primary colors each), typography, logo URLs. |
| `GET` | `/api/v1/app/branches-atms` | Nearby branches, ATMs, and CDMs with distance, operating hours, and geo coordinates. |

### 2. Authentication & Verification
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/app/auth/login` | Login via MPIN, Password, or Biometrics. |
| `POST` | `/api/v1/app/auth/mpin/verify` | Verify 4/6-digit customer MPIN. |
| `POST` | `/api/v1/app/auth/mpin/set` | Set or update MPIN with OTP verification. |
| `POST` | `/api/v1/app/auth/biometric/verify` | Verify signed hardware biometric token. |
| `POST` | `/api/v1/app/auth/biometric/register` | Register device biometric cryptographic public key. |
| `POST` | `/api/v1/app/auth/otp/send` | Trigger SMS/Email OTP for login or transaction authorization. |
| `POST` | `/api/v1/app/auth/otp/verify` | Validate OTP code. |
| `POST` | `/api/v1/app/auth/register` | Self-service digital onboarding with KYC & CIF validation (PRD US-01). |
| `POST` | `/api/v1/app/auth/forgot-password` | Account recovery & password reset flow. |

### 3. Dashboard (Composite Screen API)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/app/dashboard` | **Master dashboard endpoint** delivering greeting, account balances carousel, quick actions, 16 banking service modules, credit card outstanding widget, recent transactions, upcoming payments, and pre-approved personal loan offers. |

### 4. Accounts & Statements
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/app/accounts` | List all Savings and Current accounts with balances and status. |
| `GET` | `/api/v1/app/accounts/{account_number}` | Detailed 360-degree account profile (balances, branch, IFSC, nominees). |
| `GET` | `/api/v1/app/accounts/{account_number}/mini-statement` | Mini statement (last 5 transactions). |
| `GET` | `/api/v1/app/accounts/{account_number}/statement` | Paginated transaction ledger with date filters. |
| `GET` | `/api/v1/app/accounts/{account_number}/statement/download` | Download statement in PDF, Excel, or CSV format (PRD US-08). |
| `GET` | `/api/v1/app/accounts/{account_number}/limits` | View daily UPI, IMPS, and NEFT/RTGS transaction limits. |
| `PUT` | `/api/v1/app/accounts/{account_number}/limits` | Update daily transfer limits. |
| `GET` | `/api/v1/app/accounts/{account_number}/funds-in-clearing` | Inquire uncleared CTS cheque deposits. |
| `GET` | `/api/v1/app/recent-transactions` | Dedicated endpoint for recent transaction history with payment mode filters. |
| `GET` | `/api/v1/app/upcoming-payments` | Dedicated endpoint for scheduled dues, EMIs, and utility bills. |

### 5. Fund Transfers & Beneficiaries
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/app/transfers/transfer-types` | List transfer rails: Within Bank, IMPS, NEFT, RTGS. |
| `POST` | `/api/v1/app/transfers/initiate` | **Unified fund transfer initiation** (Screen 4 match) returning UTR, reference number, and updated balance. |
| `POST` | `/api/v1/app/transfers/within-bank` | Direct transfer between Bharat Bank accounts. |
| `POST` | `/api/v1/app/transfers/imps` | Instant 24x7 IMPS transfer. |
| `POST` | `/api/v1/app/transfers/neft` | Batch settlement NEFT transfer. |
| `POST` | `/api/v1/app/transfers/rtgs` | Real-time gross settlement transfer (min ₹2,00,000). |
| `POST` | `/api/v1/app/transfers/quick-transfer` | Ad-hoc transfer without saving payee (max ₹25,000). |
| `POST` | `/api/v1/app/transfers/schedule` | Set up scheduled one-time or recurring transfer (PRD US-11). |
| `GET` | `/api/v1/app/transfers/scheduled` | List active standing instructions and scheduled transfers. |
| `DELETE` | `/api/v1/app/transfers/scheduled/{schedule_id}` | Cancel scheduled transfer. |
| `GET` | `/api/v1/app/transfers/lookup-ifsc/{ifsc_code}` | Auto-lookup bank, branch name, address, and supported rails. |
| `GET` | `/api/v1/app/beneficiaries` | List saved payees with search (Screen 3 match). |
| `POST` | `/api/v1/app/beneficiaries` | Add new beneficiary with cooling-off period enforcement (PRD US-09). |
| `GET` | `/api/v1/app/beneficiaries/{beneficiary_id}` | Fetch beneficiary details. |
| `DELETE` | `/api/v1/app/beneficiaries/{beneficiary_id}` | Remove beneficiary. |
| `POST` | `/api/v1/app/beneficiaries/validate-account` | NPCI Penny-drop bank account verification. |

### 6. Cards, Deposits, Loans & BBPS Utilities
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/app/cards` | List Credit & Debit cards with outstanding dues and limits. |
| `POST` | `/api/v1/app/cards/{card_id}/lock-toggle` | Instant lock/unlock debit/credit card (PRD US-16). |
| `POST` | `/api/v1/app/cards/{card_id}/block` | Permanent block/hotlisting of card with reissuance option. |
| `POST` | `/api/v1/app/cards/{card_id}/pay-bill` | Pay credit card bill (Signature Mastercard due ₹67,500). |
| `GET` | `/api/v1/app/deposits` | List customer Term Deposits (FD / RD). |
| `GET` | `/api/v1/app/deposits/rates` | View interest rate slabs matrix. |
| `POST` | `/api/v1/app/deposits/calculate` | Maturity value and interest calculator. |
| `POST` | `/api/v1/app/deposits/open-fd` | Open instant online Fixed Deposit (PRD US-12). |
| `GET` | `/api/v1/app/deposits/{deposit_id}/advice` | Download official FD advice certificate PDF. |
| `GET` | `/api/v1/app/loans` | View loan accounts, outstanding balances, and next EMI date (PRD US-14). |
| `GET` | `/api/v1/app/loans/offers` | Pre-approved loan offers (Personal loan up to ₹5,00,000). |
| `GET` | `/api/v1/app/loans/{loan_id}/repayment-schedule` | Amortization schedule. |
| `POST` | `/api/v1/app/loans/{loan_id}/standing-instruction` | Setup auto-debit standing instruction for EMI (PRD US-15). |
| `POST` | `/api/v1/app/loans/apply` | Submit new loan application. |
| `GET` | `/api/v1/app/bills/categories` | List BBPS biller categories (Electricity, Mobile, DTH, Fastag, etc.). |
| `GET` | `/api/v1/app/bills/billers` | List billers by category. |
| `POST` | `/api/v1/app/bills/fetch-bill` | Fetch due bill from BBPS central switch. |
| `POST` | `/api/v1/app/bills/pay` | Pay utility bill via BBPS (PRD US-18). |
| `POST` | `/api/v1/app/cheques/request-book` | Order new cheque book (25, 50, 100 leaves) (PRD US-17). |
| `POST` | `/api/v1/app/cheques/stop-cheque` | Stop payment on specific cheque leaf (PRD US-17). |
| `GET` | `/api/v1/app/cheques/leaves` | Inquire status of cheque leaves (USED, AVAILABLE, STOPPED). |
| `GET` | `/api/v1/app/services/nominee` | View registered nominee. |
| `PUT` | `/api/v1/app/services/nominee` | Update nominee details. |
| `GET` | `/api/v1/app/services/share-ifsc` | Shareable account, IFSC card & UPI QR code. |
| `GET` | `/api/v1/app/services/nach-mandates` | List active eNACH recurring mandates. |
| `GET` | `/api/v1/app/services/epassbook` | Offline sync ePassbook entries. |
| `GET` | `/api/v1/app/services/certificates/interest` | Download Form 16A Interest Certificate. |
| `GET` | `/api/v1/app/services/certificates/tds` | Download Form 26AS TDS Certificate. |

---

## 🖥️ Collection 2: React Admin Console API Endpoints (`/api/v1/admin`)

### 1. User & Role Management (PRD US-20)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/users` | List admin staff users with roles and departments. |
| `POST` | `/api/v1/admin/users` | Create new administrative user with assigned RBAC role. |
| `GET` | `/api/v1/admin/users/roles` | List roles (Super Admin, Ops Checker, Compliance Officer, Branch Manager) and permission sets. |
| `PUT` | `/api/v1/admin/users/{user_id}/toggle-active` | Activate / deactivate admin user. |

### 2. Customer & CIF Management (PRD US-21, US-02)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/customers` | Search customer directory across CIFs, names, segments, and KYC status. |
| `GET` | `/api/v1/admin/customers/{cif}` | **Customer 360 view** consolidating demographics, accounts, cards, loans, deposits, and risk profile. |
| `POST` | `/api/v1/admin/customers/onboard` | Admin-assisted branch customer onboarding (PRD US-02). |
| `POST` | `/api/v1/admin/customers/cif-linkage` | Link or unlink CIF to digital banking mobile identity (PRD US-21). |
| `PUT` | `/api/v1/admin/customers/{cif}/status` | Freeze, block, or activate customer digital profile. |

### 3. Authorization Rules & Corporate Hierarchies (PRD US-22, US-03)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/auth-rules` | List configured maker-checker approval rules, threshold limits, and tiers. |
| `POST` | `/api/v1/admin/auth-rules` | Configure new payment approval matrix rule. |
| `GET` | `/api/v1/admin/auth-rules/corporate-hierarchies` | View corporate customer approval hierarchies and user limits (PRD US-03). |

### 4. Operations, Monitoring & System Health
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/operations/transactions` | Real-time monitoring stream of payment switch transactions. |
| `POST` | `/api/v1/admin/operations/transactions/{txn_id}/status-override` | Manual ops status override with mandatory audit reason. |
| `GET` | `/api/v1/admin/operations/service-requests` | List pending customer service requests (Cheque book, card replacement, etc.). |
| `PUT` | `/api/v1/admin/operations/service-requests/{req_id}/action` | Approve, reject, or dispatch service requests. |
| `GET` | `/api/v1/admin/operations/system-health` | Real-time health monitoring of CBS, Switch, BBPS, SMS, UIDAI, and NSDL. |

### 5. Reports & Dynamic Theming (PRD US-23)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/reports/audit-logs` | Immutable audit trail explorer of all staff and system modifications. |
| `GET` | `/api/v1/admin/reports/customer-summary` | High-level customer volume and balance analytics. |
| `POST` | `/api/v1/admin/reports/export` | Export transaction or audit reports to CSV, Excel, or PDF. |
| `GET` | `/api/v1/admin/theme-config` | View active mobile app dynamic styling and branding assets. |
| `PUT` | `/api/v1/admin/theme-config` | Real-time dynamic updates of theme colors, logos, and typography pushed to mobile clients. |

---

## 🏛️ Additional CBS Backoffice Admin APIs (`/api/v1/admin`)

### 1. CBS Account Servicing & Controls (Connecting to CBS v3)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/cbs-accounts` | List & filter accounts across CBS repository (type, status, branch, balance). |
| `POST` | `/api/v1/admin/cbs-accounts/{account_number}/freeze` | Freeze account (DEBIT, CREDIT, FULL, LIEN) with reason code (`KYC_PENDING`, `COURT_ORDER`, etc.). |
| `POST` | `/api/v1/admin/cbs-accounts/{account_number}/unfreeze` | Restore frozen account to ACTIVE in CBS. |
| `GET` | `/api/v1/admin/cbs-accounts/{account_number}/liens` | View active collateral and court attachment liens. |
| `POST` | `/api/v1/admin/cbs-accounts/{account_number}/liens` | Earmark lien amount and restrict available balance in CBS. |
| `DELETE` | `/api/v1/admin/cbs-accounts/{account_number}/liens/{lien_id}` | Release lien hold and restore available balance. |
| `POST` | `/api/v1/admin/cbs-accounts/{account_number}/balance-adjustment` | Maker-checker manual ledger adjustment against GL suspense accounts. |

### 2. Loan Underwriting & RPM Origination (Oracle OBDX / CBS v3)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/loans-underwriting/applications` | Inquire loan origination applications from OBDX/RPM engine. |
| `GET` | `/api/v1/admin/loans-underwriting/applications/{app_no}` | Full 360 application details, CIBIL score, FOIR, and applicant domain data. |
| `GET` | `/api/v1/admin/loans-underwriting/applications/{app_no}/documents` | Document verification checklist (KYC, income slips, collateral deeds). |
| `PUT` | `/api/v1/admin/loans-underwriting/applications/{app_no}/documents/{doc_id}/verify` | Mark checklist document as VERIFIED or REJECTED. |
| `POST` | `/api/v1/admin/loans-underwriting/applications/{app_no}/decision` | Issue final underwriting sanction letter or rejection with reason code. |
| `POST` | `/api/v1/admin/loans-underwriting/applications/{app_no}/disburse` | Trigger CBS loan account creation and disbursement into customer account. |

### 3. Cheque Clearing & CTS House Operations (CBS v3)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/cbs-cheques/inward-clearing` | Inward CTS clearing batch queue awaiting debit settlement. |
| `POST` | `/api/v1/admin/cbs-cheques/inward-clearing/{cheque_id}/action` | Authorize cheque clearance or return with RBI return reason codes. |
| `GET` | `/api/v1/admin/cbs-cheques/inventory` | Inquire branch vault stock of 25, 50, and 100-leaf cheque books. |
| `POST` | `/api/v1/admin/cbs-cheques/inventory/replenish` | Record cheque book stock replenishment into branch vault. |

### 4. Branch Master & Safe Deposit Lockers (CBS v3)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/cbs-branches-lockers/branches` | CBS branch directory, branch managers, vault cash holding, and locker capacities. |
| `GET` | `/api/v1/admin/cbs-branches-lockers/lockers` | Safe Deposit Locker inventory and rental matrix (SMALL, MEDIUM, LARGE, EXTRA_LARGE). |
| `POST` | `/api/v1/admin/cbs-branches-lockers/lockers/allot` | Allot vacant locker to customer CIF, set operating instructions, and collect rent. |

### 5. Term Deposits Pre-Closure Operations (CBS v3)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/cbs-deposits` | Inquire all customer term deposits across branches. |
| `GET` | `/api/v1/admin/cbs-deposits/{deposit_id}/trial-closure` | Calculate premature closure penalty, accrued interest, and net payable. |
| `POST` | `/api/v1/admin/cbs-deposits/{deposit_id}/force-close` | Execute premature closure and disburse funds to savings account. |

### 6. Daily Settlement & NPCI Reconciliation
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/cbs-reconciliation/batches` | List daily clearing cycles across IMPS, NEFT, RTGS, and BBPS. |
| `POST` | `/api/v1/admin/cbs-reconciliation/batches/{batch_id}/reconcile` | Run automated 3-way reconciliation (CBS vs Switch vs NPCI). |
| `GET` | `/api/v1/admin/cbs-reconciliation/exceptions` | Inquire unmatched transactions and settlement discrepancies. |
| `POST` | `/api/v1/admin/cbs-reconciliation/exceptions/{exception_id}/resolve` | Execute automatic refund or ledger adjustment to resolve exception. |
