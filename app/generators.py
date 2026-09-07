import random
import datetime
from typing import Dict, Any

FIRST_NAMES = ["John", "Jane", "Rahul", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Rohan", "Deepika"]
LAST_NAMES = ["Doe", "Smith", "Sharma", "Patel", "Verma", "Gupta", "Kumar", "Singh", "Reddy", "Mehta"]
BENEFICIARIES = ["ABC TRADERS", "RELIANCE POWER", "AIRTEL TELECOM", "AMAZON RETAIL", "FLIPKART LOGISTICS", "METRO WATER", "CITY GAS CORP"]
PRODUCT_CODES = ["SB001", "SB002", "CA001", "CA002", "TD001", "SALARY01"]
STATUSES = ["ACTIVE", "INACTIVE", "DORMANT", "FROZEN"]
CARD_STATUSES = ["ACTIVE", "BLOCKED", "HOTLISTED", "EXPIRED"]
CHEQUE_STATUSES = ["ISSUED", "CLEARED", "PASSED", "STOPPED", "RETURNED"]


def rand_cif() -> str:
    return f"CIF{random.randint(100000, 999999)}"


def rand_account_num() -> str:
    return f"101{random.randint(100000000, 999999999)}"


def rand_amount(min_val=100.0, max_val=500000.0) -> float:
    return round(random.uniform(min_val, max_val), 2)


def rand_date(days_back=60) -> str:
    d = datetime.date.today() - datetime.timedelta(days=random.randint(0, days_back))
    return d.strftime("%Y-%m-%d")


def rand_future_date(days_ahead=60) -> str:
    d = datetime.date.today() + datetime.timedelta(days=random.randint(1, days_ahead))
    return d.strftime("%Y-%m-%d")


def generate_random_customer_account_inquiry(req_cif: str = None) -> Dict[str, Any]:
    cif = req_cif or rand_cif()
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    ledger = rand_amount(10000, 500000)
    avail = round(ledger - random.uniform(100, 5000), 2)
    return {
        "Customer": {
            "CustomerId": cif,
            "CustomerName": f"{first} {last}",
            "CustomerType": random.choice(["INDIVIDUAL", "CORPORATE", "NRI"]),
            "MobileNumber": f"9{random.randint(100000000, 999999999)}",
            "EmailId": f"{first.lower()}.{last.lower()}@email.com",
            "KycStatus": random.choice(["COMPLETED", "VERIFIED"])
        },
        "Accounts": {
            "Account": [
                {
                    "AccountNumber": rand_account_num(),
                    "AccountType": random.choice(["SAVINGS", "CURRENT"]),
                    "Currency": "INR",
                    "LedgerBalance": ledger,
                    "AvailableBalance": avail,
                    "Status": "ACTIVE",
                    "JointHolders": {
                        "JointHolder": [
                            {
                                "CustomerId": rand_cif(),
                                "Name": f"{random.choice(FIRST_NAMES)} {last}"
                            }
                        ]
                    },
                    "Nominees": {
                        "Nominee": [
                            {
                                "Name": f"Nominee {random.choice(FIRST_NAMES)}",
                                "Relation": random.choice(["SPOUSE", "FATHER", "MOTHER", "CHILD"]),
                                "SharePercentage": 100
                            }
                        ]
                    }
                }
            ]
        }
    }


def generate_random_customer_account_basic(req_cif: str = None) -> Dict[str, Any]:
    cif = req_cif or rand_cif()
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return {
        "Customer": {
            "CustomerId": cif,
            "CustomerName": f"{first} {last}"
        },
        "Accounts": {
            "Account": [
                {
                    "AccountNumber": rand_account_num(),
                    "AccountType": random.choice(["SAVINGS", "CURRENT"]),
                    "AvailableBalance": rand_amount(5000, 200000)
                }
            ]
        }
    }


def generate_random_account_details(req_acc: str = None) -> Dict[str, Any]:
    acc = req_acc or rand_account_num()
    return {
        "Account": {
            "AccountNumber": acc,
            "ProductCode": random.choice(PRODUCT_CODES),
            "Currency": "INR",
            "Status": random.choice(["ACTIVE", "INACTIVE"])
        },
        "Cards": {
            "Card": [
                {
                    "CardNumber": f"XXXXXX{random.randint(1000, 9999)}",
                    "CardType": random.choice(["DEBIT", "CREDIT"]),
                    "Status": random.choice(CARD_STATUSES),
                    "ExpiryDate": f"{random.randint(2027, 2032)}-{random.randint(1, 12):02d}-28"
                }
            ]
        },
        "RelatedParties": {
            "RelatedParty": [
                {
                    "CustomerId": rand_cif(),
                    "Relationship": "JOINT_HOLDER"
                }
            ]
        },
        "Nominees": {
            "Nominee": [
                {
                    "Name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                }
            ]
        }
    }


def generate_random_opening_balance(req_acc: str = None, as_on: str = None) -> Dict[str, Any]:
    return {
        "AccountId": req_acc or rand_account_num(),
        "OpeningBalance": rand_amount(10000, 300000),
        "Currency": "INR"
    }


def generate_random_freeze(req_acc: str = None, freeze_type: str = "DEBIT") -> Dict[str, Any]:
    ref = f"FRZ{random.randint(100000, 999999)}"
    return {
        "Status": "SUCCESS",
        "ReferenceNumber": ref,
        "Message": f"Account {freeze_type} Freeze Successful"
    }


def generate_random_unfreeze(req_acc: str = None) -> Dict[str, Any]:
    ref = f"UNF{random.randint(100000, 999999)}"
    return {
        "Status": "SUCCESS",
        "ReferenceNumber": ref,
        "Message": "Account Unfreeze Successful"
    }


def generate_random_card_update(req_card: str = None, new_status: str = "BLOCKED") -> Dict[str, Any]:
    ref = f"CRD{random.randint(100000, 999999)}"
    return {
        "Status": "SUCCESS",
        "ReferenceNumber": ref,
        "Message": f"Card Status Updated to {new_status}"
    }


def generate_random_cheque_issued_summary(cif: str = None) -> Dict[str, Any]:
    count = random.randint(3, 30)
    total = round(count * random.uniform(1000, 25000), 2)
    return {
        "TotalCheques": count,
        "TotalAmount": total
    }


def generate_random_cheque_issued_details(cif: str = None) -> Dict[str, Any]:
    count = random.randint(1, 5)
    cheques = []
    for _ in range(count):
        cheques.append({
            "ChequeNumber": str(random.randint(100001, 199999)),
            "IssueDate": rand_date(30),
            "Amount": rand_amount(1000, 50000),
            "Status": random.choice(CHEQUE_STATUSES),
            "Beneficiary": random.choice(BENEFICIARIES)
        })
    return {"Cheques": {"Cheque": cheques}}


def generate_random_cheque_deposited_summary(cif: str = None) -> Dict[str, Any]:
    count = random.randint(1, 15)
    total = round(count * random.uniform(5000, 30000), 2)
    return {
        "TotalCheques": count,
        "TotalAmount": total
    }


def generate_random_cheque_deposited_details(cif: str = None) -> Dict[str, Any]:
    count = random.randint(1, 4)
    cheques = []
    for _ in range(count):
        cheques.append({
            "ChequeNumber": str(random.randint(500001, 599999)),
            "DepositDate": rand_date(20),
            "Amount": rand_amount(2000, 40000),
            "Status": random.choice(["CLEARED", "IN_PROCESS", "RETURNED"])
        })
    return {"Cheques": {"Cheque": cheques}}


def generate_random_cheque_status(acc: str = None, chq: str = None) -> Dict[str, Any]:
    return {
        "ChequeNumber": chq or str(random.randint(100001, 199999)),
        "Status": random.choice(["PASSED", "STOPPED", "CLEARED", "RETURNED", "ISSUED"]),
        "Amount": rand_amount(1000, 20000),
        "TransactionDate": rand_date(10)
    }


def generate_random_interest_cert(cif: str = None, year: str = "2026") -> Dict[str, Any]:
    return {
        "CustomerId": cif or rand_cif(),
        "FinancialYear": year or "2026",
        "InterestEarned": rand_amount(5000, 50000)
    }


def generate_random_tds_cert(cif: str = None, year: str = "2026") -> Dict[str, Any]:
    interest = rand_amount(5000, 50000)
    tds = round(interest * 0.10, 2)
    return {
        "CustomerId": cif or rand_cif(),
        "FinancialYear": year or "2026",
        "TDSDeducted": tds
    }


def generate_random_locker_inquiry(branch: str = None) -> Dict[str, Any]:
    return {
        "Lockers": {
            "Locker": [
                {
                    "LockerType": "SMALL",
                    "AvailableCount": random.randint(5, 50),
                    "AnnualRent": 1500.0
                },
                {
                    "LockerType": "MEDIUM",
                    "AvailableCount": random.randint(2, 20),
                    "AnnualRent": 3000.0
                },
                {
                    "LockerType": "LARGE",
                    "AvailableCount": random.randint(0, 10),
                    "AnnualRent": 5000.0
                }
            ]
        }
    }


def generate_random_mobile_validation(cif: str = None, mobile: str = None) -> Dict[str, Any]:
    is_valid = random.choice([True, True, True, False])
    return {
        "Valid": is_valid,
        "Message": "Mobile Number Matched" if is_valid else "Mobile Number Not Matched"
    }


def generate_random_td_trial_closure(acc: str = None) -> Dict[str, Any]:
    val = rand_amount(50000, 200000)
    penalty = round(random.uniform(200, 1000), 2)
    return {
        "TDAccountId": acc or f"TD{random.randint(100000, 999999)}",
        "ClosureValue": val,
        "PenaltyAmount": penalty,
        "NetPayable": round(val - penalty, 2)
    }


def generate_random_upcoming_payments(cif: str = None) -> Dict[str, Any]:
    types = ["EMI", "BILL_PAYMENT", "SI", "INSURANCE"]
    return {
        "Payments": {
            "Payment": [
                {
                    "PaymentType": random.choice(types),
                    "DueDate": rand_future_date(30),
                    "Amount": rand_amount(1000, 25000)
                }
            ]
        }
    }


def generate_random_upcoming_income(cif: str = None) -> Dict[str, Any]:
    types = ["FD_INTEREST", "SALARY", "DIVIDEND", "RENTAL_INCOME"]
    return {
        "Incomes": {
            "Income": [
                {
                    "IncomeType": random.choice(types),
                    "CreditDate": rand_future_date(30),
                    "Amount": rand_amount(5000, 75000)
                }
            ]
        }
    }


def generate_random_cheque_leaves_status(acc: str = None) -> Dict[str, Any]:
    start_num = random.randint(110000, 990000)
    leaves = [
        {"ChequeNumber": str(start_num + 1), "Status": "USED"},
        {"ChequeNumber": str(start_num + 2), "Status": "USED"},
        {"ChequeNumber": str(start_num + 3), "Status": "AVAILABLE"},
        {"ChequeNumber": str(start_num + 4), "Status": "AVAILABLE"},
        {"ChequeNumber": str(start_num + 5), "Status": "STOPPED"}
    ]
    return {"Cheques": {"Cheque": leaves}}
