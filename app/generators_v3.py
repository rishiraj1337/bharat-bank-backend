import random
import datetime
from typing import Dict, Any, Optional

FIRST_NAMES = ["John", "Jane", "Rahul", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Rohan", "Deepika"]
LAST_NAMES = ["Doe", "Smith", "Sharma", "Patel", "Verma", "Gupta", "Kumar", "Singh", "Reddy", "Mehta"]
BENEFICIARIES = ["ABC TRADERS", "RELIANCE POWER", "AIRTEL TELECOM", "AMAZON RETAIL", "FLIPKART LOGISTICS", "METRO WATER", "CITY GAS CORP"]
PRODUCT_CODES = ["SB001", "SB002", "CA001", "CA002", "TD001", "SALARY01"]


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


def rand_amount(min_val=100.0, max_val=500000.0) -> float:
    return round(random.uniform(min_val, max_val), 2)


def generate_v3_customer_account_inquiry(req_cif: str = None) -> Dict[str, Any]:
    cif = req_cif or rand_cif()
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    ledger = rand_amount(50000, 500000)
    lien = round(random.choice([0.0, 1000.0, 2000.0, 5000.0]), 2)
    avail = round(ledger - lien, 2)
    acc_num = rand_account_num()

    return {
        "Customer": {
            "CustomerId": cif,
            "CustomerName": f"{first} {last}",
            "CustomerType": "INDIVIDUAL",
            "MobileNumber": f"9{random.randint(100000000, 999999999)}",
            "EmailId": f"{first.lower()}.{last.lower()}@email.com",
            "KycStatus": "COMPLETED"
        },
        "Accounts": {
            "Account": [
                {
                    "AccountNumber": acc_num,
                    "AccountType": "SAVINGS",
                    "ProductCode": "SB001",
                    "ProductName": "Premium Savings Account",
                    "Currency": "INR",
                    "BranchCode": "001",
                    "BranchName": "Main Metro Branch",
                    "IFSC": "OBDX0000001",
                    "MICR": "110002001",
                    "LedgerBalance": ledger,
                    "AvailableBalance": avail,
                    "LienAmount": lien,
                    "UnclearedBalance": 0.0,
                    "InterestRate": 4.5,
                    "Status": "ACTIVE",
                    "OpenDate": "2024-01-15",
                    "NomineeRegistered": True,
                    "ChequeBookFacility": True,
                    "DebitCardActive": True,
                    "JointHolders": {
                        "JointHolder": [
                            {
                                "CustomerId": rand_cif(),
                                "Name": f"{random.choice(FIRST_NAMES)} {last}",
                                "Relationship": "JOINT_HOLDER"
                            }
                        ]
                    },
                    "Nominees": {
                        "Nominee": [
                            {
                                "Name": f"Nominee {random.choice(FIRST_NAMES)}",
                                "Relation": "SPOUSE",
                                "SharePercentage": 100
                            }
                        ]
                    },
                    "Cards": {
                        "Card": [
                            {
                                "CardNumber": f"XXXXXX{random.randint(1000, 9999)}",
                                "CardType": "DEBIT",
                                "Status": "ACTIVE",
                                "ExpiryDate": "2029-12-31"
                            }
                        ]
                    }
                }
            ]
        }
    }


def generate_v3_customer_account_basic(req_cif: str = None) -> Dict[str, Any]:
    cif = req_cif or rand_cif()
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    avail = rand_amount(5000, 200000)
    return {
        "Customer": {
            "CustomerId": cif,
            "CustomerName": f"{first} {last}",
            "CustomerType": "INDIVIDUAL",
            "MobileNumber": f"9{random.randint(100000000, 999999999)}",
            "EmailId": f"{first.lower()}@email.com",
            "KycStatus": "COMPLETED"
        },
        "Accounts": {
            "Account": [
                {
                    "AccountNumber": rand_account_num(),
                    "AccountType": "SAVINGS",
                    "AvailableBalance": avail,
                    "LedgerBalance": round(avail + 2000.0, 2),
                    "Currency": "INR"
                }
            ]
        }
    }


def generate_v3_account_details(req_acc: str = None) -> Dict[str, Any]:
    acc = req_acc or rand_account_num()
    ledger = rand_amount(50000, 300000)
    lien = 2000.0
    return {
        "Account": {
            "AccountNumber": acc,
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
        },
        "Cards": {
            "Card": [
                {
                    "CardNumber": f"XXXXXX{random.randint(1000, 9999)}",
                    "CardType": "DEBIT",
                    "Status": "ACTIVE",
                    "ExpiryDate": "2029-12-31"
                }
            ]
        },
        "RelatedParties": {
            "RelatedParty": [
                {
                    "CustomerId": rand_cif(),
                    "Name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                    "Relationship": "JOINT_HOLDER"
                }
            ]
        },
        "Nominees": {
            "Nominee": [
                {
                    "Name": "Nominee One",
                    "Relation": "SPOUSE",
                    "SharePercentage": 100
                }
            ]
        }
    }


def generate_v3_account_statements(req_acc: str = None, from_date: str = None, to_date: str = None, offset: int = 0, limit: int = 10) -> Dict[str, Any]:
    acc = req_acc or rand_account_num()
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
    tot_dr = 0.0
    tot_cr = 0.0

    for i, (ttype, narr, amt) in enumerate(narrations):
        if ttype == "DEBIT":
            running_bal -= amt
            tot_dr += amt
        else:
            running_bal += amt
            tot_cr += amt
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
        "TotalDebits": round(tot_dr, 2),
        "TotalCredits": round(tot_cr, 2),
        "Transactions": {
            "Transaction": txns
        },
        "Paging": {
            "totalResults": len(txns),
            "offset": offset,
            "limit": limit
        }
    }


def generate_v3_loans_inquiry(req_cif: str = None) -> Dict[str, Any]:
    return {
        "CustomerId": req_cif or rand_cif(),
        "Loans": {
            "Loan": [
                {
                    "LoanAccountNumber": rand_loan_acc(),
                    "LoanType": "HOME_LOAN",
                    "SanctionedAmount": 5000000.00,
                    "OutstandingPrincipal": 4250000.00,
                    "InterestRate": 8.5,
                    "TenureMonths": 240,
                    "RemainingTenureMonths": 195,
                    "EMIAmount": 43391.00,
                    "NextDueDate": "2026-09-10",
                    "Status": "ACTIVE"
                }
            ]
        }
    }


def generate_v3_loan_schedule(req_loan: str = None) -> Dict[str, Any]:
    acc = req_loan or rand_loan_acc()
    sched = []
    bal = 4250000.0
    rate = 8.5
    emi = 43391.0

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
        "Schedule": {
            "Installment": sched
        }
    }


def generate_v3_deposits_inquiry(req_cif: str = None) -> Dict[str, Any]:
    return {
        "CustomerId": req_cif or rand_cif(),
        "Deposits": {
            "Deposit": [
                {
                    "DepositAccountNumber": rand_deposit_acc(),
                    "DepositType": "FIXED_DEPOSIT",
                    "PrincipalAmount": 200000.00,
                    "InterestRate": 7.25,
                    "MaturityAmount": 231800.00,
                    "DepositDate": "2025-09-04",
                    "MaturityDate": "2027-09-04",
                    "InterestPayout": "ON_MATURITY",
                    "AutoRenewal": True,
                    "Status": "ACTIVE"
                }
            ]
        }
    }
