import random
import datetime
from typing import Dict, Any, Optional

FIRST_NAMES = ["John", "Jane", "Rahul", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Rohan", "Deepika"]
LAST_NAMES = ["Doe", "Smith", "Sharma", "Patel", "Verma", "Gupta", "Kumar", "Singh", "Reddy", "Mehta"]


def rand_cif() -> str:
    return f"CIF{random.randint(100000, 999999)}"


def rand_account_num() -> str:
    return f"101{random.randint(100000000, 999999999)}"


def rand_loan_acc() -> str:
    return f"LN{random.randint(1000000000, 9999999999)}"


def rand_deposit_acc() -> str:
    return f"FD{random.randint(1000000000, 9999999999)}"


def rand_app_num() -> str:
    return f"APP2026{random.randint(10000000, 99999999)}"


def rand_ref_num(prefix="REF") -> str:
    return f"{prefix}{random.randint(10000000, 99999999)}"


def generate_random_businessproducts(product_type: str = None, channel: str = "OBDX") -> Dict[str, Any]:
    types = [product_type] if product_type else ["LOAN", "SAVINGS", "TERM_DEPOSIT", "CURRENT"]
    products = []
    
    for ptype in types:
        if ptype == "LOAN":
            code = "HL001"
            name = "Prime Home Loan"
            subtype = "HOME_LOAN"
            min_amt, max_amt = 500000.0, 10000000.0
            min_term, max_term = 12, 360
        elif ptype == "SAVINGS":
            code = "SB001"
            name = "Smart Advantage Savings"
            subtype = "SAVINGS_ACCOUNT"
            min_amt, max_amt = 1000.0, 5000000.0
            min_term, max_term = 0, 0
        elif ptype == "TERM_DEPOSIT":
            code = "TD001"
            name = "High Yield Term Deposit"
            subtype = "FIXED_DEPOSIT"
            min_amt, max_amt = 10000.0, 10000000.0
            min_term, max_term = 3, 120
        else:
            code = "CA001"
            name = "Trade Plus Current Account"
            subtype = "CURRENT_ACCOUNT"
            min_amt, max_amt = 25000.0, 50000000.0
            min_term, max_term = 0, 0

        products.append({
            "businessProductDetails": {
                "businessProductCode": code,
                "businessProductName": name,
                "businessProductDesc": f"Comprehensive {name} solution tailored for modern digital banking.",
                "productType": ptype,
                "productSubType": subtype,
                "startDate": "2026-01-01",
                "expiryDate": "2030-12-31"
            },
            "businessProductPreferences": {
                "businessProductCode": code,
                "productType": ptype,
                "productSubType": subtype,
                "channelAllowed": "Y",
                "minAge": 18,
                "maxAge": 70,
                "BusProdPrefComp": {
                    "autoRollover": "Y",
                    "chequebook": "Y",
                    "debitcard": "Y",
                    "directBanking": "Y",
                    "passbook": "Y",
                    "phoneBanking": "Y",
                    "BusProdCcyConfig": [
                        {
                            "currency": "INR",
                            "minAmount": min_amt,
                            "maxAmount": max_amt,
                            "minTerm": min_term,
                            "maxTerm": max_term,
                            "minTermTenorBasis": "M",
                            "maxTermTenorBasis": "M"
                        }
                    ],
                    "IntlScrCrdDecnboxDTO": [
                        {
                            "scorecardType": "INTERNAL",
                            "minScore": 650.0,
                            "maxScore": 900.0,
                            "outcome": "ACCEPT",
                            "serialNo": 1
                        }
                    ]
                }
            },
            "businessProductAttr": {
                "businessProductCode": code,
                "productType": ptype,
                "businessProductSummary": f"Competitive rates and premium features for {name}.",
                "BusProdAttrFeature": [
                    {
                        "businessProductCode": code,
                        "featureName": "Instant Digital Approval",
                        "featureDesc": "Zero paperwork end-to-end digital journey"
                    }
                ],
                "BusProdAttrFeeCharges": [
                    {
                        "businessProductCode": code,
                        "feeChargesName": "Standard Processing Fee",
                        "feeChargesDesc": "0.25% - 0.50% depending on profile"
                    }
                ]
            }
        })

    return {
        "data": products,
        "paging": {
            "totalResults": len(products),
            "offset": 0,
            "limit": 10
        }
    }


def generate_random_process_initiate(ptype="LOAN", channel="OBDX") -> Dict[str, Any]:
    app_no = rand_app_num()
    prc_ref = rand_ref_num("PRC")
    return {
        "messages": {
            "id": rand_ref_num("MSG"),
            "status": "SUCCESS",
            "codes": [{"Code": "00", "Desc": "Process initiated successfully", "Type": "I"}],
            "requestId": rand_ref_num("REQ")
        },
        "applicationNumber": app_no,
        "processRefNo": prc_ref,
        "status": "INITIATED"
    }


def generate_random_process_submit(app_no=None) -> Dict[str, Any]:
    app_num = app_no or rand_app_num()
    return {
        "messages": {
            "id": rand_ref_num("MSG"),
            "status": "SUCCESS",
            "codes": [{"Code": "00", "Desc": "Application submitted successfully", "Type": "I"}],
            "requestId": rand_ref_num("REQ")
        },
        "applicationNumber": app_num,
        "status": "SUBMITTED"
    }


def generate_random_process_get_data(app_no=None) -> Dict[str, Any]:
    app_num = app_no or rand_app_num()
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return {
        "channel": "OBDX",
        "action": "SUBMIT",
        "applicationNumber": app_num,
        "remarks": "Verified and passed initial risk screening",
        "domainData": {
            "CmnApplicant": {
                "firstName": first,
                "lastName": last,
                "mobile": f"9{random.randint(100000000, 999999999)}",
                "email": f"{first.lower()}@email.com",
                "pan": "ABCDE1234F"
            },
            "LoanAccOpenProcess": [
                {
                    "requestedAmount": 2500000.0,
                    "tenureMonths": 120,
                    "purpose": "Home Renovation"
                }
            ]
        }
    }


def generate_random_document_list(app_no=None, product_type="LOAN") -> Dict[str, Any]:
    return {
        "data": [
            {"documentId": "DOC001", "documentName": "PAN Card Copy", "documentType": "KYC_IDENTITY", "mandatory": "Y", "status": "VERIFIED"},
            {"documentId": "DOC002", "documentName": "Aadhaar / Passport", "documentType": "KYC_ADDRESS", "mandatory": "Y", "status": "VERIFIED"},
            {"documentId": "DOC003", "documentName": "Last 6 Months Bank Statement", "documentType": "INCOME_PROOF", "mandatory": "Y", "status": "PENDING"},
            {"documentId": "DOC004", "documentName": "Salary Slip / Form 16", "documentType": "INCOME_PROOF", "mandatory": "N", "status": "PENDING"}
        ]
    }


def generate_random_applications_list(offset=0, limit=10) -> Dict[str, Any]:
    items = []
    statuses = ["INITIATED", "IN_PROGRESS", "APPROVED", "REJECTED", "DISBURSED"]
    products = [("LOAN", "Prime Home Loan"), ("SAVINGS", "Smart Savings"), ("LOAN", "Auto Loan"), ("TERM_DEPOSIT", "High Yield TD")]

    for i in range(min(5, limit)):
        ptype, pname = random.choice(products)
        items.append({
            "applicationNo": f"APP2026{random.randint(10000000, 99999999)}",
            "processRefNo": f"PRC{random.randint(10000000, 99999999)}",
            "applicationDate": (datetime.date.today() - datetime.timedelta(days=i*2)).strftime("%Y-%m-%d"),
            "productType": ptype,
            "productSubType": ptype,
            "businessProductName": pname,
            "custName": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "custMobile": f"9{random.randint(100000000, 999999999)}",
            "custEmail": "customer@email.com",
            "branchCode": "001",
            "channel": "OBDX",
            "status": random.choice(statuses)
        })

    return {
        "data": items,
        "paging": {
            "totalResults": len(items),
            "offset": offset,
            "limit": limit
        }
    }


def generate_random_account_info_360(acc_id=None) -> Dict[str, Any]:
    acc = acc_id or rand_account_num()
    ledger = round(random.uniform(50000, 500000), 2)
    lien = round(random.choice([0.0, 1000.0, 2500.0, 5000.0]), 2)
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return {
        "AccountId": acc,
        "AccountNumber": acc,
        "CustomerId": rand_cif(),
        "CustomerName": f"{first} {last}",
        "AccountType": "SAVINGS",
        "ProductCode": "SB001",
        "ProductName": "Premium Savings Account",
        "Currency": "INR",
        "BranchCode": "001",
        "BranchName": "Main Metro Branch",
        "IFSC": "OBDX0000001",
        "MICR": "110002001",
        "LedgerBalance": ledger,
        "AvailableBalance": round(ledger - lien, 2),
        "LienAmount": lien,
        "UnclearedBalance": 0.0,
        "InterestRate": 4.5,
        "Status": "ACTIVE",
        "OpenDate": "2024-01-15",
        "NomineeRegistered": True,
        "ChequeBookFacility": True,
        "DebitCardActive": True
    }


def generate_random_account_statement(acc_id=None, from_date=None, to_date=None) -> Dict[str, Any]:
    acc = acc_id or rand_account_num()
    f_date = from_date or (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    t_date = to_date or datetime.date.today().strftime("%Y-%m-%d")
    
    running_bal = round(random.uniform(100000, 200000), 2)
    opening_bal = running_bal
    txns = []
    narrations = [
        ("DEBIT", "UPI/Swiggy/Food Delivery", 450.0),
        ("DEBIT", "ATM Cash Withdrawal", 5000.0),
        ("CREDIT", "Salary Credit / Tech Corp", 75000.0),
        ("DEBIT", "Amazon Online Shopping", 2499.0),
        ("CREDIT", "FD Interest Credit", 3450.0),
        ("DEBIT", "Electricity Utility Bill Payment", 1850.0)
    ]

    total_debits = 0.0
    total_credits = 0.0

    for i, (ttype, narr, amt) in enumerate(narrations):
        if ttype == "DEBIT":
            running_bal -= amt
            total_debits += amt
        else:
            running_bal += amt
            total_credits += amt
        
        tx_date = (datetime.date.today() - datetime.timedelta(days=len(narrations) - i)).strftime("%Y-%m-%d")
        txns.append({
            "TransactionId": f"TXN2026{random.randint(10000000, 99999999)}",
            "TransactionDate": tx_date,
            "ValueDate": tx_date,
            "Type": ttype,
            "Amount": amt,
            "Currency": "INR",
            "BalanceAfter": round(running_bal, 2),
            "Narration": narr,
            "ReferenceNo": f"REF{random.randint(1000000, 9999999)}",
            "Channel": "MOBILE"
        })

    return {
        "AccountId": acc,
        "FromDate": f_date,
        "ToDate": t_date,
        "OpeningBalance": round(opening_bal, 2),
        "ClosingBalance": round(running_bal, 2),
        "TotalDebits": round(total_debits, 2),
        "TotalCredits": round(total_credits, 2),
        "Transactions": txns,
        "Paging": {
            "totalResults": len(txns),
            "offset": 0,
            "limit": 10
        }
    }


def generate_random_loan_accounts(cif=None) -> Dict[str, Any]:
    return {
        "CustomerId": cif or rand_cif(),
        "Loans": [
            {
                "LoanAccountNumber": rand_loan_acc(),
                "LoanType": "HOME_LOAN",
                "SanctionedAmount": 4500000.0,
                "OutstandingPrincipal": 3850000.0,
                "InterestRate": 8.4,
                "TenureMonths": 240,
                "RemainingTenureMonths": 180,
                "EMIAmount": 38780.0,
                "NextDueDate": (datetime.date.today() + datetime.timedelta(days=12)).strftime("%Y-%m-%d"),
                "Status": "ACTIVE"
            },
            {
                "LoanAccountNumber": rand_loan_acc(),
                "LoanType": "AUTO_LOAN",
                "SanctionedAmount": 800000.0,
                "OutstandingPrincipal": 420000.0,
                "InterestRate": 9.1,
                "TenureMonths": 60,
                "RemainingTenureMonths": 28,
                "EMIAmount": 16650.0,
                "NextDueDate": (datetime.date.today() + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                "Status": "ACTIVE"
            }
        ]
    }


def generate_random_loan_schedule(loan_acc=None) -> Dict[str, Any]:
    acc = loan_acc or rand_loan_acc()
    sched = []
    bal = 3850000.0
    rate = 8.4
    emi = 38780.0
    
    for i in range(1, 13):
        int_comp = round(bal * (rate / 1200.0), 2)
        prin_comp = round(emi - int_comp, 2)
        bal = round(bal - prin_comp, 2)
        due = (datetime.date.today() + datetime.timedelta(days=i*30)).strftime("%Y-%m-%d")
        sched.append({
            "InstallmentNo": i,
            "DueDate": due,
            "PrincipalComponent": prin_comp,
            "InterestComponent": int_comp,
            "TotalInstallment": emi,
            "EndingBalance": max(0.0, bal)
        })

    return {
        "LoanAccountNumber": acc,
        "InterestRate": rate,
        "Schedule": sched
    }


def generate_random_loan_apply(cif=None, loan_type="HOME_LOAN", amount=2000000.0, tenure=120) -> Dict[str, Any]:
    rate = 8.5
    r = (rate / 1200.0)
    emi = round(amount * r * ((1 + r) ** tenure) / (((1 + r) ** tenure) - 1), 2)
    return {
        "ApplicationNumber": f"LNAPP2026{random.randint(100000, 999999)}",
        "Status": "IN_REVIEW",
        "EstimatedEMI": emi,
        "Message": f"Loan application for {loan_type} received successfully. Processing Reference: REF{random.randint(100000, 999999)}"
    }


def generate_random_deposit_accounts(cif=None) -> Dict[str, Any]:
    return {
        "CustomerId": cif or rand_cif(),
        "Deposits": [
            {
                "DepositAccountNumber": rand_deposit_acc(),
                "DepositType": "FIXED_DEPOSIT",
                "PrincipalAmount": 250000.0,
                "InterestRate": 7.25,
                "MaturityAmount": 288300.0,
                "DepositDate": "2025-08-10",
                "MaturityDate": "2027-08-10",
                "InterestPayout": "ON_MATURITY",
                "AutoRenewal": True,
                "Status": "ACTIVE"
            },
            {
                "DepositAccountNumber": rand_deposit_acc(),
                "DepositType": "RECURRING_DEPOSIT",
                "PrincipalAmount": 10000.0,
                "InterestRate": 6.9,
                "MaturityAmount": 125500.0,
                "DepositDate": "2026-01-01",
                "MaturityDate": "2027-01-01",
                "InterestPayout": "MONTHLY_INSTALLMENT",
                "AutoRenewal": False,
                "Status": "ACTIVE"
            }
        ]
    }


def generate_random_deposit_open(cif=None, amount=100000.0, tenure=12) -> Dict[str, Any]:
    rate = 7.1
    mat_amt = round(amount * (1 + (rate * (tenure / 12.0) / 100.0)), 2)
    mat_date = (datetime.date.today() + datetime.timedelta(days=tenure * 30)).strftime("%Y-%m-%d")
    return {
        "DepositAccountNumber": rand_deposit_acc(),
        "PrincipalAmount": amount,
        "InterestRate": rate,
        "MaturityAmount": mat_amt,
        "MaturityDate": mat_date,
        "Status": "ACTIVE",
        "Message": f"Term Deposit of INR {amount:,.2f} opened successfully."
    }


def generate_random_fund_transfer(debtor=None, creditor=None, amount=5000.0, mode="IMPS") -> Dict[str, Any]:
    return {
        "TransactionReference": f"FT2026{random.randint(100000000, 999999999)}",
        "Status": "SUCCESS",
        "DebtorAccount": debtor or rand_account_num(),
        "Amount": amount,
        "Currency": "INR",
        "Timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
        "UTR": f"UTR{random.randint(1000000000, 9999999999)}",
        "Message": f"Fund transfer of INR {amount:,.2f} via {mode} completed successfully."
    }
