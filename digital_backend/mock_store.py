"""
In-memory Mock Database Store for Bharat Bank Omnichannel Backend.
Preloaded with rich banking state corresponding to PRD & Mobile App Screenshots.
"""
from typing import Dict, List, Any
import copy
from datetime import datetime

class MockDataStore:
    def __init__(self):
        self.reset()

    def reset(self):
        # 1. Theme Configuration
        self.theme_config = {
            "theme_id": "bharat_bank_modern_v1",
            "theme_version": "1.2.0",
            "is_dark_mode_configured": True,
            "light_colors": {
                "primary": "#1A56DB",
                "secondary": "#3B82F6",
                "accent": "#10B981",
                "background": "#F8FAFC",
                "surface": "#FFFFFF",
                "text_primary": "#0F172A",
                "text_secondary": "#64748B",
                "border": "#E2E8F0"
            },
            "dark_colors": {
                "primary": "#3B82F6",
                "secondary": "#60A5FA",
                "accent": "#34D399",
                "background": "#0F172A",
                "surface": "#1E293B",
                "text_primary": "#F8FAFC",
                "text_secondary": "#94A3B8",
                "border": "#334155"
            },
            "typography": {
                "font_family_heading": "Inter",
                "font_family_body": "Inter",
                "heading_font_size_scale": 1.0,
                "body_font_size_scale": 1.0
            },
            "logo_url": "https://assets.bharatbank.com/branding/logo-standard.png",
            "light_logo_url": "https://assets.bharatbank.com/branding/logo-light.png",
            "dark_logo_url": "https://assets.bharatbank.com/branding/logo-dark.png",
            "favicon_url": "https://assets.bharatbank.com/branding/favicon.ico",
            "app_name": "Bharat Bank",
            "brand_tagline": "Empowering Every Indian with Smart Banking"
        }

        # 2. Customers (Retail, Corporate, NRI, Wealth)
        self.customers = {
            "CIF100001": {
                "cif": "CIF100001",
                "name": "Arjun Mehta",
                "customer_type": "RETAIL",
                "dob_or_incorporation": "1992-05-14",
                "gender": "MALE",
                "mobile_number": "9876543210",
                "email": "arjun.mehta@bharatbank.com",
                "pan_number": "ABCDE1234F",
                "aadhaar_masked": "XXXX-XXXX-9182",
                "address": "102, Palm Heights, Bandra West, Mumbai 400050",
                "kyc_status": "VERIFIED",
                "kyc_verified_on": "2024-01-16",
                "digital_profile_status": "ACTIVE",
                "risk_rating": "LOW",
                "home_branch": "Nariman Point (001)",
                "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
                "last_login": "Today, 09:42 AM",
                "mpin": "1234",
                "biometric_enabled": True
            },
            "CIF100002": {
                "cif": "CIF100002",
                "name": "Sneha Mehta",
                "customer_type": "RETAIL",
                "dob_or_incorporation": "1994-08-22",
                "gender": "FEMALE",
                "mobile_number": "9876543211",
                "email": "sneha.mehta@gmail.com",
                "pan_number": "BCDEF2345G",
                "aadhaar_masked": "XXXX-XXXX-8821",
                "address": "102, Palm Heights, Bandra West, Mumbai 400050",
                "kyc_status": "VERIFIED",
                "kyc_verified_on": "2024-02-10",
                "digital_profile_status": "ACTIVE",
                "risk_rating": "LOW",
                "home_branch": "Nariman Point (001)",
                "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
                "last_login": "Yesterday, 04:15 PM"
            },
            "CIF100003": {
                "cif": "CIF100003",
                "name": "Vikramaditya Rao",
                "customer_type": "NRI",
                "dob_or_incorporation": "1985-03-12",
                "gender": "MALE",
                "mobile_number": "+971501234567",
                "email": "vikram.rao@dubaiholding.ae",
                "pan_number": "CDEFG3456H",
                "aadhaar_masked": "XXXX-XXXX-4412",
                "address": "Villa 14, Emirates Hills, Dubai, UAE",
                "kyc_status": "VERIFIED",
                "kyc_verified_on": "2023-11-05",
                "digital_profile_status": "ACTIVE",
                "risk_rating": "LOW",
                "home_branch": "Overseas Banking Branch, BKC (005)",
                "last_login": "04 Sep 2026, 11:20 AM"
            },
            "CIF-CORP-9001": {
                "cif": "CIF-CORP-9001",
                "name": "Nexus Tech Enterprises Pvt Ltd",
                "customer_type": "CORPORATE",
                "dob_or_incorporation": "2018-06-25",
                "gender": "ORGANIZATION",
                "mobile_number": "9820011223",
                "email": "finance@nexustech.com",
                "pan_number": "AABCN9918K",
                "aadhaar_masked": "GSTIN: 27AABCN9918K1Z5",
                "address": "Level 8, Nexus One Cyber Tower, BKC, Mumbai 400051",
                "kyc_status": "VERIFIED",
                "kyc_verified_on": "2023-08-14",
                "digital_profile_status": "ACTIVE",
                "risk_rating": "MEDIUM",
                "home_branch": "BKC Metro Branch (002)",
                "last_login": "Today, 08:30 AM"
            },
            "CIF-CORP-9002": {
                "cif": "CIF-CORP-9002",
                "name": "ABC Global Logistics LLP",
                "customer_type": "CORPORATE",
                "dob_or_incorporation": "2020-01-10",
                "gender": "ORGANIZATION",
                "mobile_number": "9833445566",
                "email": "accounts@abcgloballogistics.com",
                "pan_number": "AABCU7721L",
                "aadhaar_masked": "GSTIN: 27AABCU7721L1Z2",
                "address": "Plot 45, MIDC Industrial Area, Andheri East, Mumbai 400093",
                "kyc_status": "VERIFIED",
                "kyc_verified_on": "2024-03-01",
                "digital_profile_status": "ACTIVE",
                "risk_rating": "MEDIUM",
                "home_branch": "Andheri Corporate Hub (003)",
                "last_login": "Yesterday, 06:45 PM"
            }
        }

        # 3. Accounts Portfolio
        self.accounts = {
            "101000000012": {
                "account_id": "ACC-101000000012",
                "cif": "CIF100001",
                "account_number": "101000000012",
                "masked_account_number": "**** **** 0012",
                "account_type": "Savings Account",
                "account_type_code": "SAVINGS",
                "product_code": "SB001",
                "product_name": "Premium Savings Account",
                "status": "Active",
                "available_balance": 482450.00,
                "ledger_balance": 482450.00,
                "currency": "INR",
                "currency_symbol": "₹",
                "ifsc": "APEX0001048",
                "micR": "400002001",
                "branch_code": "001",
                "branch_name": "Nariman Point Branch",
                "interest_rate": "6.5% p.a.",
                "is_primary": True,
                "open_date": "2024-01-15",
                "nominee_name": "Sneha Mehta",
                "cheque_facility": True,
                "daily_upi_limit": 100000.00,
                "daily_imps_limit": 500000.00,
                "daily_neft_rtgs_limit": 2000000.00
            },
            "101000009943": {
                "account_id": "ACC-101000009943",
                "cif": "CIF100001",
                "account_number": "101000009943",
                "masked_account_number": "**** **** 9943",
                "account_type": "Current Account",
                "account_type_code": "CURRENT",
                "product_code": "CA001",
                "product_name": "Smart Business Current Account",
                "status": "Active",
                "available_balance": 1195000.00,
                "ledger_balance": 1195000.00,
                "currency": "INR",
                "currency_symbol": "₹",
                "ifsc": "APEX0001048",
                "micr": "400002001",
                "branch_code": "001",
                "branch_name": "Nariman Point Branch",
                "interest_rate": None,
                "is_primary": False,
                "open_date": "2024-03-10",
                "daily_upi_limit": 200000.00,
                "daily_imps_limit": 1000000.00,
                "daily_neft_rtgs_limit": 5000000.00
            },
            "101000005521": {
                "account_id": "ACC-101000005521",
                "cif": "CIF100001",
                "account_number": "101000005521",
                "masked_account_number": "**** **** 5521",
                "account_type": "Salary Account",
                "account_type_code": "SALARY",
                "product_code": "SL001",
                "product_name": "Corporate Platinum Salary Account",
                "status": "Active",
                "available_balance": 225000.00,
                "ledger_balance": 225000.00,
                "currency": "INR",
                "currency_symbol": "₹",
                "ifsc": "APEX0001048",
                "branch_code": "001",
                "branch_name": "Nariman Point Branch",
                "interest_rate": "4.0% p.a.",
                "is_primary": False,
                "open_date": "2024-06-01",
                "daily_upi_limit": 100000.00,
                "daily_imps_limit": 500000.00,
                "daily_neft_rtgs_limit": 2000000.00
            },
            "202000001188": {
                "account_id": "ACC-202000001188",
                "cif": "CIF-CORP-9001",
                "account_number": "202000001188",
                "masked_account_number": "**** **** 1188",
                "account_type": "Corporate Current Account",
                "account_type_code": "CURRENT",
                "product_code": "CA002",
                "product_name": "Enterprise Premier Current Account",
                "status": "Active",
                "available_balance": 45890000.00,
                "ledger_balance": 45890000.00,
                "currency": "INR",
                "currency_symbol": "₹",
                "ifsc": "APEX0001002",
                "branch_code": "002",
                "branch_name": "BKC Metro Branch",
                "interest_rate": None,
                "is_primary": True,
                "open_date": "2023-08-15"
            }
        }

        # 4. Beneficiaries Directory (Expanded)
        self.beneficiaries = [
            {
                "beneficiary_id": "BEN-001",
                "cif": "CIF100001",
                "name": "Sneha Mehta",
                "bank_name": "Bharat Co-operative Bank",
                "account_number": "99182390129182",
                "masked_account_number": "**** **** 9182",
                "ifsc": "BCOB0001234",
                "account_type": "SAVINGS",
                "transfer_type": "IMPS",
                "avatar_initials": "SM",
                "is_within_bank": False,
                "cooling_period_active": False,
                "max_transfer_limit": 500000.00
            },
            {
                "beneficiary_id": "BEN-002",
                "cif": "CIF100001",
                "name": "Rohan Deshmukh",
                "bank_name": "HDFC Bank",
                "account_number": "50100239488239",
                "masked_account_number": "**** **** 8239",
                "ifsc": "HDFC0000456",
                "account_type": "SAVINGS",
                "transfer_type": "IMPS",
                "avatar_initials": "RD",
                "is_within_bank": False,
                "cooling_period_active": False,
                "max_transfer_limit": 500000.00
            },
            {
                "beneficiary_id": "BEN-003",
                "cif": "CIF100001",
                "name": "Amitabh Bachchan",
                "bank_name": "ICICI Bank",
                "account_number": "00071092830007",
                "masked_account_number": "**** **** 0007",
                "ifsc": "ICIC0000108",
                "account_type": "SAVINGS",
                "transfer_type": "RTGS",
                "avatar_initials": "AB",
                "is_within_bank": False,
                "cooling_period_active": False,
                "max_transfer_limit": 2000000.00
            },
            {
                "beneficiary_id": "BEN-004",
                "cif": "CIF100001",
                "name": "ABC Suppliers Ltd.",
                "bank_name": "HDFC Bank",
                "account_number": "50200088997821",
                "masked_account_number": "**** 7821",
                "ifsc": "HDFC0000999",
                "account_type": "CURRENT",
                "transfer_type": "NEFT",
                "avatar_initials": "AS",
                "is_within_bank": False,
                "cooling_period_active": False,
                "max_transfer_limit": 5000000.00
            },
            {
                "beneficiary_id": "BEN-005",
                "cif": "CIF100001",
                "name": "Amazon Web Services",
                "bank_name": "Citibank",
                "account_number": "02938102938182",
                "masked_account_number": "**** 8182",
                "ifsc": "CITI0000002",
                "account_type": "CURRENT",
                "transfer_type": "NEFT",
                "avatar_initials": "AW",
                "is_within_bank": False,
                "cooling_period_active": False,
                "max_transfer_limit": 10000000.00
            },
            {
                "beneficiary_id": "BEN-006",
                "cif": "CIF100001",
                "name": "Kavita Sharma",
                "bank_name": "State Bank of India",
                "account_number": "309988112233",
                "masked_account_number": "**** **** 2233",
                "ifsc": "SBIN0000300",
                "account_type": "SAVINGS",
                "transfer_type": "IMPS",
                "avatar_initials": "KS",
                "is_within_bank": False,
                "cooling_period_active": False,
                "max_transfer_limit": 500000.00
            },
            {
                "beneficiary_id": "BEN-007",
                "cif": "CIF100001",
                "name": "Sunil V. Pillai",
                "bank_name": "Bharat Bank",
                "account_number": "101000008833",
                "masked_account_number": "**** **** 8833",
                "ifsc": "APEX0001048",
                "account_type": "SAVINGS",
                "transfer_type": "WITHIN_BANK",
                "avatar_initials": "SP",
                "is_within_bank": True,
                "cooling_period_active": False,
                "max_transfer_limit": 1000000.00
            }
        ]

        # 5. Cards Portfolio (Credit & Debit & Forex)
        self.cards = [
            {
                "card_id": "CRD-3349",
                "cif": "CIF100001",
                "card_number": "5412750012343349",
                "masked_card_number": "**** **** **** 3349",
                "card_holder_name": "Arjun Mehta",
                "card_type": "CREDIT",
                "card_network": "Mastercard",
                "card_name": "Signature Mastercard",
                "expiry_date": "12/29",
                "cvv": "***",
                "is_locked": False,
                "is_blocked": False,
                "credit_limit": 200000.00,
                "available_credit_limit": 132500.00,
                "outstanding_due": 67500.00,
                "formatted_outstanding_due": "₹67,500",
                "due_date": "2026-09-18",
                "due_in_text": "Due in 11 days",
                "cta_text": "Pay Card Bill",
                "domestic_pos_enabled": True,
                "domestic_online_enabled": True,
                "international_enabled": False,
                "contactless_enabled": True
            },
            {
                "card_id": "CRD-1234",
                "cif": "CIF100001",
                "card_number": "4111110022331234",
                "masked_card_number": "**** **** **** 1234",
                "card_holder_name": "Arjun Mehta",
                "card_type": "DEBIT",
                "card_network": "RuPay",
                "card_name": "Platinum Debit Card",
                "expiry_date": "08/30",
                "cvv": "***",
                "linked_account_number": "101000000012",
                "is_locked": False,
                "is_blocked": False,
                "credit_limit": None,
                "available_credit_limit": None,
                "outstanding_due": 0.0,
                "domestic_pos_enabled": True,
                "domestic_online_enabled": True,
                "international_enabled": True,
                "contactless_enabled": True
            },
            {
                "card_id": "CRD-8821",
                "cif": "CIF100001",
                "card_number": "4218900011228821",
                "masked_card_number": "**** **** **** 8821",
                "card_holder_name": "Arjun Mehta",
                "card_type": "DEBIT",
                "card_network": "Visa",
                "card_name": "Visa Infinite Multi-Currency Forex Card",
                "expiry_date": "05/31",
                "cvv": "***",
                "linked_account_number": "101000000012",
                "is_locked": False,
                "is_blocked": False,
                "credit_limit": None,
                "available_credit_limit": None,
                "outstanding_due": 0.0,
                "domestic_pos_enabled": False,
                "domestic_online_enabled": True,
                "international_enabled": True,
                "contactless_enabled": True
            }
        ]

        # 6. Detailed Rich Transaction History
        self.transactions = [
            {
                "transaction_id": "TXN-20260907-001",
                "reference_no": "POS-APPLE-88291",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "Apple Store Mumbai BKC",
                "subtitle": "Today, 10:14 AM • Card",
                "date_formatted": "Today, 10:14 AM",
                "transaction_date": "2026-09-07",
                "value_date": "2026-09-07",
                "narration": "Apple Store Mumbai BKC - POS Purchase",
                "payment_mode": "Card",
                "channel": "CARD",
                "amount": 14500.00,
                "formatted_amount": "-₹14,500",
                "type": "DEBIT",
                "status": "Success",
                "category": "Shopping",
                "balance_after": 482450.00,
                "icon": "arrow_outward"
            },
            {
                "transaction_id": "TXN-20260906-002",
                "reference_no": "UPI-SBX-991823",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "Starbucks Coffee Reserve",
                "subtitle": "Yesterday, 07:30 PM • UPI",
                "date_formatted": "Yesterday, 07:30 PM",
                "transaction_date": "2026-09-06",
                "value_date": "2026-09-06",
                "narration": "UPI/starbucks@icici/Coffee Reserve",
                "payment_mode": "UPI",
                "channel": "MOBILE",
                "amount": 1250.00,
                "formatted_amount": "-₹1,250",
                "type": "DEBIT",
                "status": "Success",
                "category": "Dining",
                "balance_after": 496950.00,
                "icon": "arrow_outward"
            },
            {
                "transaction_id": "TXN-20260815-003",
                "reference_no": "NEFT-NEXUS-88219",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "Monthly Salary Credit – Nexus Tech",
                "subtitle": "15 Aug 2026 • NEFT",
                "date_formatted": "15 Aug 2026",
                "transaction_date": "2026-08-15",
                "value_date": "2026-08-15",
                "narration": "NEFT/NEXUS TECH SALARY AUGUST 2026",
                "payment_mode": "NEFT",
                "channel": "NEFT",
                "amount": 225000.00,
                "formatted_amount": "+₹2,25,000",
                "type": "CREDIT",
                "status": "Success",
                "category": "Salary",
                "balance_after": 498200.00,
                "icon": "arrow_downward"
            },
            {
                "transaction_id": "TXN-20260814-004",
                "reference_no": "UPI-ADANI-443912",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "Adani Electricity Mumbai",
                "subtitle": "14 Aug 2026 • UPI",
                "date_formatted": "14 Aug 2026",
                "transaction_date": "2026-08-14",
                "value_date": "2026-08-14",
                "narration": "UPI/adanienergy@axis/Electricity Bill Mumbai",
                "payment_mode": "UPI",
                "channel": "MOBILE",
                "amount": 4500.00,
                "formatted_amount": "-₹4,500",
                "type": "DEBIT",
                "status": "Success",
                "category": "Utilities",
                "balance_after": 273200.00,
                "icon": "arrow_outward"
            },
            {
                "transaction_id": "TXN-20260812-005",
                "reference_no": "IMPS-SIP-102938",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "Bharat Bluechip Flexi SIP",
                "subtitle": "12 Aug 2026 • IMPS",
                "date_formatted": "12 Aug 2026",
                "transaction_date": "2026-08-12",
                "value_date": "2026-08-12",
                "narration": "IMPS/BHARAT AMC/BLUECHIP FLEXI SIP",
                "payment_mode": "IMPS",
                "channel": "MOBILE",
                "amount": 25000.00,
                "formatted_amount": "-₹25,000",
                "type": "DEBIT",
                "status": "Success",
                "category": "Investment",
                "balance_after": 277700.00,
                "icon": "arrow_outward"
            },
            {
                "transaction_id": "TXN-20260810-006",
                "reference_no": "UPI-SWIGGY-881923",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "Swiggy Gourmet Food Delivery",
                "subtitle": "10 Aug 2026 • UPI",
                "date_formatted": "10 Aug 2026",
                "transaction_date": "2026-08-10",
                "value_date": "2026-08-10",
                "narration": "UPI/swiggy@icici/Order #9812903",
                "payment_mode": "UPI",
                "channel": "MOBILE",
                "amount": 1420.00,
                "formatted_amount": "-₹1,420",
                "type": "DEBIT",
                "status": "Success",
                "category": "Dining",
                "balance_after": 302700.00,
                "icon": "arrow_outward"
            },
            {
                "transaction_id": "TXN-20260805-007",
                "reference_no": "FD-INT-991823",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "Quarterly Term Deposit Interest Credit",
                "subtitle": "05 Aug 2026 • INT",
                "date_formatted": "05 Aug 2026",
                "transaction_date": "2026-08-05",
                "value_date": "2026-08-05",
                "narration": "INT CR/FD-1010000091/Q1 INTEREST",
                "payment_mode": "CBS_TRANSFER",
                "channel": "SYSTEM",
                "amount": 3625.00,
                "formatted_amount": "+₹3,625",
                "type": "CREDIT",
                "status": "Success",
                "category": "Interest",
                "balance_after": 304120.00,
                "icon": "arrow_downward"
            },
            {
                "transaction_id": "TXN-20260802-008",
                "reference_no": "ATM-WDL-109283",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "ATM Cash Withdrawal - Bandra West",
                "subtitle": "02 Aug 2026 • ATM",
                "date_formatted": "02 Aug 2026",
                "transaction_date": "2026-08-02",
                "value_date": "2026-08-02",
                "narration": "ATM/WDL/APEX-ATM-002/MUMBAI",
                "payment_mode": "Card",
                "channel": "ATM",
                "amount": 10000.00,
                "formatted_amount": "-₹10,000",
                "type": "DEBIT",
                "status": "Success",
                "category": "Cash",
                "balance_after": 300495.00,
                "icon": "arrow_outward"
            },
            {
                "transaction_id": "TXN-20260728-009",
                "reference_no": "UPI-AMAZON-552109",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "Amazon Online Marketplace",
                "subtitle": "28 Jul 2026 • UPI",
                "date_formatted": "28 Jul 2026",
                "transaction_date": "2026-07-28",
                "value_date": "2026-07-28",
                "narration": "UPI/amazonpay@axis/Order 402-1928301",
                "payment_mode": "UPI",
                "channel": "MOBILE",
                "amount": 8990.00,
                "formatted_amount": "-₹8,990",
                "type": "DEBIT",
                "status": "Success",
                "category": "Shopping",
                "balance_after": 310495.00,
                "icon": "arrow_outward"
            },
            {
                "transaction_id": "TXN-20260715-010",
                "reference_no": "NEFT-NEXUS-77182",
                "account_number": "101000000012",
                "cif": "CIF100001",
                "title": "Monthly Salary Credit – Nexus Tech",
                "subtitle": "15 Jul 2026 • NEFT",
                "date_formatted": "15 Jul 2026",
                "transaction_date": "2026-07-15",
                "value_date": "2026-07-15",
                "narration": "NEFT/NEXUS TECH SALARY JULY 2026",
                "payment_mode": "NEFT",
                "channel": "NEFT",
                "amount": 225000.00,
                "formatted_amount": "+₹2,25,000",
                "type": "CREDIT",
                "status": "Success",
                "category": "Salary",
                "balance_after": 319485.00,
                "icon": "arrow_downward"
            }
        ]

        # 7. Upcoming Payments (Expanded)
        self.upcoming_payments = [
            {
                "id": "UPAY-001",
                "cif": "CIF100001",
                "title": "Signature Mastercard Bill",
                "biller_or_payee": "Bharat Bank Credit Cards",
                "amount": 67500.00,
                "formatted_amount": "₹67,500.00",
                "due_date": "2026-09-18",
                "due_in_days": 11,
                "type": "CREDIT_CARD",
                "is_autopay_enabled": False
            },
            {
                "id": "UPAY-002",
                "cif": "CIF100001",
                "title": "Prime Home Loan EMI",
                "biller_or_payee": "Bharat Bank Retail Assets",
                "amount": 43391.00,
                "formatted_amount": "₹43,391.00",
                "due_date": "2026-09-10",
                "due_in_days": 3,
                "type": "LOAN_EMI",
                "is_autopay_enabled": True
            },
            {
                "id": "UPAY-003",
                "cif": "CIF100001",
                "title": "Adani Electricity Monthly Bill",
                "biller_or_payee": "Adani Electricity Mumbai",
                "amount": 4500.00,
                "formatted_amount": "₹4,500.00",
                "due_date": "2026-09-20",
                "due_in_days": 13,
                "type": "UTILITY_BILL",
                "is_autopay_enabled": False
            },
            {
                "id": "UPAY-004",
                "cif": "CIF100001",
                "title": "HDFC Life Super Shield Premium",
                "biller_or_payee": "HDFC Life Insurance",
                "amount": 25000.00,
                "formatted_amount": "₹25,000.00",
                "due_date": "2026-09-25",
                "due_in_days": 18,
                "type": "NACH_MANDATE",
                "is_autopay_enabled": True
            },
            {
                "id": "UPAY-005",
                "cif": "CIF100001",
                "title": "Airtel Fiber Broadband Bill",
                "biller_or_payee": "Bharti Airtel Limited",
                "amount": 1179.00,
                "formatted_amount": "₹1,179.00",
                "due_date": "2026-09-28",
                "due_in_days": 21,
                "type": "UTILITY_BILL",
                "is_autopay_enabled": False
            }
        ]

        # 8. Term Deposits (FD, RD, Tax Saver)
        self.deposits = [
            {
                "deposit_id": "FD-1010000091",
                "cif": "CIF100001",
                "account_number": "FD1010000091",
                "deposit_type": "FIXED_DEPOSIT",
                "principal_amount": 200000.00,
                "formatted_principal": "₹2,00,000.00",
                "interest_rate": 7.25,
                "maturity_amount": 231800.00,
                "formatted_maturity": "₹2,31,800.00",
                "deposit_date": "2025-09-07",
                "maturity_date": "2027-09-07",
                "tenure_months": 24,
                "interest_payout_mode": "ON_MATURITY",
                "auto_renewal": True,
                "nominee_name": "Sneha Mehta",
                "status": "ACTIVE"
            },
            {
                "deposit_id": "RD-1010000092",
                "cif": "CIF100001",
                "account_number": "RD1010000092",
                "deposit_type": "RECURRING_DEPOSIT",
                "principal_amount": 10000.00,
                "formatted_principal": "₹10,000.00/month",
                "interest_rate": 7.00,
                "maturity_amount": 130500.00,
                "formatted_maturity": "₹1,30,500.00",
                "deposit_date": "2026-01-01",
                "maturity_date": "2027-01-01",
                "tenure_months": 12,
                "interest_payout_mode": "ON_MATURITY",
                "auto_renewal": False,
                "nominee_name": "Sneha Mehta",
                "status": "ACTIVE"
            },
            {
                "deposit_id": "FD-1010000093",
                "cif": "CIF100001",
                "account_number": "FD1010000093",
                "deposit_type": "TAX_SAVER_FD",
                "principal_amount": 150000.00,
                "formatted_principal": "₹1,50,000.00",
                "interest_rate": 7.50,
                "maturity_amount": 215450.00,
                "formatted_maturity": "₹2,15,450.00",
                "deposit_date": "2024-03-31",
                "maturity_date": "2029-03-31",
                "tenure_months": 60,
                "interest_payout_mode": "ON_MATURITY",
                "auto_renewal": False,
                "nominee_name": "Sneha Mehta",
                "status": "ACTIVE"
            }
        ]

        # 9. Loans (Home, Personal, Auto)
        self.loans = [
            {
                "loan_id": "LN-101000001",
                "cif": "CIF100001",
                "loan_account_number": "LN101000001",
                "loan_type": "HOME_LOAN",
                "sanctioned_amount": 5000000.00,
                "formatted_sanctioned": "₹50,00,000.00",
                "outstanding_principal": 4250000.00,
                "formatted_outstanding": "₹42,50,000.00",
                "interest_rate": 8.50,
                "emi_amount": 43391.00,
                "formatted_emi": "₹43,391.00",
                "next_due_date": "2026-09-10",
                "total_tenure_months": 240,
                "remaining_tenure_months": 195,
                "auto_pay_linked_account": "101000000012",
                "is_auto_pay_active": True,
                "status": "ACTIVE"
            },
            {
                "loan_id": "LN-101000002",
                "cif": "CIF100001",
                "loan_account_number": "LN101000002",
                "loan_type": "AUTO_LOAN",
                "sanctioned_amount": 1200000.00,
                "formatted_sanctioned": "₹12,00,000.00",
                "outstanding_principal": 640000.00,
                "formatted_outstanding": "₹6,40,000.00",
                "interest_rate": 8.90,
                "emi_amount": 24850.00,
                "formatted_emi": "₹24,850.00",
                "next_due_date": "2026-09-15",
                "total_tenure_months": 60,
                "remaining_tenure_months": 28,
                "auto_pay_linked_account": "101000000012",
                "is_auto_pay_active": True,
                "status": "ACTIVE"
            }
        ]

        # 10. Pre-approved Offers & Banners
        self.pre_approved_offers = [
            {
                "id": "OFFER-PL-500K",
                "badge": "PRE-APPROVED OFFER",
                "title": "Instant Personal Loan up to ₹5,00,000",
                "subtitle": "Disbursed in 30 seconds with zero paperwork.",
                "cta_text": "Avail Now",
                "cta_route": "/loans/pre-approved/apply",
                "max_amount": 500000.00,
                "interest_rate_p_a": 10.49,
                "valid_until": "2026-09-30"
            },
            {
                "id": "OFFER-CC-UPGRADE",
                "badge": "EXCLUSIVE UPGRADE",
                "title": "Upgrade to Bharat World Elite Metal Credit Card",
                "subtitle": "Complimentary airport lounge access worldwide & 5X reward points.",
                "cta_text": "Upgrade Free",
                "cta_route": "/cards/upgrade/metal",
                "max_amount": 500000.00,
                "interest_rate_p_a": 0.0,
                "valid_until": "2026-10-15"
            }
        ]

        self.banners = [
            {
                "id": "BANNER-01",
                "image_url": "https://assets.bharatbank.com/banners/fixed-deposit-fest.png",
                "title": "Special Monsoon FD Rates at 7.75% p.a. for 444 Days",
                "deeplink": "/deposits/open-fd"
            },
            {
                "id": "BANNER-02",
                "image_url": "https://assets.bharatbank.com/banners/zero-forex-card.png",
                "title": "Travel the world with Zero Forex Markup Cards",
                "deeplink": "/cards/forex/apply"
            },
            {
                "id": "BANNER-03",
                "image_url": "https://assets.bharatbank.com/banners/home-loan-balance-transfer.png",
                "title": "Transfer your Home Loan to Bharat Bank @ 8.25% p.a.",
                "deeplink": "/loans/balance-transfer"
            }
        ]

        # 11. 16 Banking Service Modules (Exact list matching Screenshot 2)
        self.banking_services = [
            {"id": "srv_accounts", "title": "Accounts", "icon": "wallet", "route": "/accounts", "category": "CORE"},
            {"id": "srv_cards", "title": "Cards", "icon": "credit_card", "route": "/cards", "category": "CORE"},
            {"id": "srv_transfer", "title": "Transfer", "icon": "swap_horiz", "route": "/transfers", "category": "PAYMENT"},
            {"id": "srv_deposits", "title": "Deposits", "icon": "savings", "route": "/deposits", "category": "INVESTMENT"},
            {"id": "srv_loans", "title": "Loans", "icon": "account_balance", "route": "/loans", "category": "BORROW"},
            {"id": "srv_cheque", "title": "Cheque", "icon": "menu_book", "route": "/cheques", "category": "SERVICES"},
            {"id": "srv_billpay", "title": "Bill Pay", "icon": "receipt_long", "route": "/bills", "category": "PAYMENT"},
            {"id": "srv_recharge", "title": "Recharge", "icon": "smartphone", "route": "/bills/recharge", "category": "PAYMENT"},
            {"id": "srv_beneficiaries", "title": "Beneficiaries", "icon": "people", "route": "/beneficiaries", "category": "PAYMENT"},
            {"id": "srv_statements", "title": "Statements", "icon": "description", "route": "/accounts/statements", "category": "SERVICES"},
            {"id": "srv_scheduled", "title": "Scheduled", "icon": "event_repeat", "route": "/transfers/scheduled", "category": "PAYMENT"},
            {"id": "srv_epassbook", "title": "ePassbook", "icon": "auto_stories", "route": "/services/epassbook", "category": "SERVICES"},
            {"id": "srv_nominee", "title": "Nominee", "icon": "account_circle", "route": "/services/nominee", "category": "PROFILE"},
            {"id": "srv_shareifsc", "title": "Share IFSC", "icon": "share", "route": "/services/share-ifsc", "category": "CORE"},
            {"id": "srv_nach", "title": "NACH", "icon": "sync_alt", "route": "/services/nach-mandates", "category": "SERVICES"},
            {"id": "srv_more", "title": "More", "icon": "layers", "route": "/services/all", "category": "MORE"}
        ]

        # 12. Quick Actions
        self.quick_actions = [
            {"id": "qa_transfer", "title": "Transfer", "icon": "swap_horiz", "route": "/transfers", "category": "PAYMENT", "badge": "Instant (24/7)"},
            {"id": "qa_paybills", "title": "Pay Bills", "icon": "flash_on", "route": "/bills", "category": "PAYMENT", "badge": "Instant (24/7)"},
            {"id": "qa_mobilepay", "title": "Send via Mobile", "icon": "smartphone", "route": "/transfers/quick-transfer", "category": "PAYMENT", "badge": "Instant (24/7)"},
            {"id": "qa_beneficiaries", "title": "Beneficiaries", "icon": "people", "route": "/beneficiaries", "category": "PAYMENT", "badge": "Instant (24/7)"}
        ]

        # 13. Admin Staff Users & Roles (PRD 6.9 US-20)
        self.admin_users = [
            {
                "user_id": "ADM-101",
                "username": "rajesh.amin",
                "full_name": "Rajesh Amin",
                "email": "rajesh.amin@bharatbank.com",
                "role": "SUPER_ADMIN",
                "department": "IT Operations",
                "branch_code": "001",
                "is_active": True,
                "last_login_at": "2026-09-07T05:30:00Z",
                "created_at": "2026-01-10T10:00:00Z"
            },
            {
                "user_id": "ADM-102",
                "username": "priya.sharma",
                "full_name": "Priya Sharma",
                "email": "priya.sharma@bharatbank.com",
                "role": "OPS_CHECKER",
                "department": "Branch Operations",
                "branch_code": "001",
                "is_active": True,
                "last_login_at": "2026-09-07T04:15:00Z",
                "created_at": "2026-02-01T11:00:00Z"
            },
            {
                "user_id": "ADM-103",
                "username": "tarun.chand",
                "full_name": "Tarun Chand",
                "email": "tarun.chand@bharatbank.com",
                "role": "COMPLIANCE_OFFICER",
                "department": "Compliance & Audit",
                "branch_code": "001",
                "is_active": True,
                "last_login_at": "2026-09-06T18:00:00Z",
                "created_at": "2026-02-15T09:30:00Z"
            },
            {
                "user_id": "ADM-104",
                "username": "chandan.kumar",
                "full_name": "Chandan Kumar",
                "email": "chandan.kumar@bharatbank.com",
                "role": "OPS_MAKER",
                "department": "Retail Customer Onboarding",
                "branch_code": "002",
                "is_active": True,
                "last_login_at": "2026-09-07T06:00:00Z",
                "created_at": "2026-03-01T08:30:00Z"
            },
            {
                "user_id": "ADM-105",
                "username": "deepak.verma",
                "full_name": "Deepak Verma",
                "email": "deepak.verma@bharatbank.com",
                "role": "BRANCH_MANAGER",
                "department": "Nariman Point Branch",
                "branch_code": "001",
                "is_active": True,
                "last_login_at": "2026-09-06T19:20:00Z",
                "created_at": "2025-11-20T10:00:00Z"
            }
        ]

        self.admin_roles = [
            {
                "role_id": "ROLE_SUPER_ADMIN",
                "role_name": "Super Administrator",
                "description": "Full unrestricted access to system configurations, admin users, and audit logs",
                "permissions": ["USERS_MANAGE", "CIF_LINK", "RULES_CONFIG", "REPORTS_EXPORT", "OVERRIDE_TXN", "THEME_MANAGE"]
            },
            {
                "role_id": "ROLE_OPS_CHECKER",
                "role_name": "Operations Checker",
                "description": "Secondary level approval for high-value client onboarding, limits, and rule changes",
                "permissions": ["CIF_LINK_APPROVE", "SERVICE_REQUEST_APPROVE", "REPORTS_VIEW"]
            },
            {
                "role_id": "ROLE_OPS_MAKER",
                "role_name": "Operations Maker",
                "description": "Front-desk initiation of client onboarding and service processing",
                "permissions": ["CIF_ONBOARD", "SERVICE_REQUEST_PROCESS"]
            },
            {
                "role_id": "ROLE_COMPLIANCE_OFFICER",
                "role_name": "Compliance & Audit Officer",
                "description": "Audit trail review, KYC re-verification, and regulatory report exports",
                "permissions": ["AUDIT_VIEW", "REPORTS_EXPORT", "KYC_VERIFY"]
            },
            {
                "role_id": "ROLE_BRANCH_MANAGER",
                "role_name": "Branch Manager",
                "description": "Branch level oversight, override approvals, and daily clearing reconciliations",
                "permissions": ["BRANCH_OVERRIDE", "CLEARING_APPROVE", "STAFF_MONITOR"]
            }
        ]

        # 14. Authorization Rules & Corporate Hierarchies (PRD 6.9 US-22)
        self.auth_rules = [
            {
                "rule_id": "RULE-CORP-TXN-01",
                "rule_name": "Corporate Payment Maker-Checker Tier 1",
                "client_segment": "CORPORATE",
                "min_amount": 100000.00,
                "max_amount": 1000000.00,
                "maker_role_required": "CORP_MAKER",
                "checker_role_required": "CORP_CHECKER_L1",
                "required_approvals_count": 1,
                "cooling_period_hours": 2,
                "is_active": True,
                "version": 2,
                "updated_by": "rajesh.amin",
                "updated_at": "2026-08-30T14:20:00Z"
            },
            {
                "rule_id": "RULE-CORP-TXN-02",
                "rule_name": "High Value Transfer Dual-Approval",
                "client_segment": "CORPORATE",
                "min_amount": 1000000.00,
                "max_amount": 10000000.00,
                "maker_role_required": "CORP_MAKER",
                "checker_role_required": "CORP_CHECKER_L2",
                "required_approvals_count": 2,
                "cooling_period_hours": 4,
                "is_active": True,
                "version": 1,
                "updated_by": "rajesh.amin",
                "updated_at": "2026-08-15T10:00:00Z"
            },
            {
                "rule_id": "RULE-RETAIL-INT-01",
                "rule_name": "Retail Cross-Border Remittance Dual Verification",
                "client_segment": "RETAIL",
                "min_amount": 500000.00,
                "max_amount": 2500000.00,
                "maker_role_required": "SYSTEM_TRIGGER",
                "checker_role_required": "FOREX_CHECKER",
                "required_approvals_count": 1,
                "cooling_period_hours": 12,
                "is_active": True,
                "version": 1,
                "updated_by": "tarun.chand",
                "updated_at": "2026-09-01T09:00:00Z"
            }
        ]

        self.corporate_hierarchies = [
            {
                "hierarchy_id": "CORP-HIER-01",
                "corporate_cif": "CIF-CORP-9001",
                "corporate_name": "Nexus Tech Enterprises Pvt Ltd",
                "login_id": "nexus.cfo",
                "employee_name": "Vikram Sengupta",
                "tier_level": 1,
                "daily_limit": 10000000.00,
                "per_txn_limit": 2500000.00,
                "can_initiate": True,
                "can_approve": True,
                "status": "ACTIVE"
            },
            {
                "hierarchy_id": "CORP-HIER-02",
                "corporate_cif": "CIF-CORP-9001",
                "corporate_name": "Nexus Tech Enterprises Pvt Ltd",
                "login_id": "nexus.acc_manager",
                "employee_name": "Anita Roy",
                "tier_level": 2,
                "daily_limit": 2500000.00,
                "per_txn_limit": 500000.00,
                "can_initiate": True,
                "can_approve": False,
                "status": "ACTIVE"
            },
            {
                "hierarchy_id": "CORP-HIER-03",
                "corporate_cif": "CIF-CORP-9002",
                "corporate_name": "ABC Global Logistics LLP",
                "login_id": "abc.managing_partner",
                "employee_name": "Harish Bhat",
                "tier_level": 1,
                "daily_limit": 50000000.00,
                "per_txn_limit": 10000000.00,
                "can_initiate": True,
                "can_approve": True,
                "status": "ACTIVE"
            }
        ]

        # 15. Service Requests (PRD 6.7, 6.9)
        self.service_requests = [
            {
                "request_id": "SR-202609-0012",
                "cif": "CIF100001",
                "customer_name": "Arjun Mehta",
                "request_type": "CHEQUE_BOOK_ISSUE",
                "details": {"account_number": "101000000012", "leaves": 50, "delivery_address": "102, Palm Heights, Bandra West, Mumbai"},
                "submitted_at": "2026-09-07T04:20:00Z",
                "status": "PENDING",
                "assigned_to": "rajesh.amin"
            },
            {
                "request_id": "SR-202609-0011",
                "cif": "CIF100001",
                "customer_name": "Arjun Mehta",
                "request_type": "ESTATEMENT_REGISTRATION",
                "details": {"account_number": "101000000012", "frequency": "MONTHLY", "email": "arjun.mehta@bharatbank.com"},
                "submitted_at": "2026-09-05T10:15:00Z",
                "status": "COMPLETED",
                "assigned_to": "priya.sharma"
            },
            {
                "request_id": "SR-202609-0010",
                "cif": "CIF100002",
                "customer_name": "Sneha Mehta",
                "request_type": "CARD_UPGRADE",
                "details": {"current_card": "CRD-1234", "requested_variant": "Bharat Metal Signature", "annual_income": "2500000"},
                "submitted_at": "2026-09-06T15:40:00Z",
                "status": "IN_PROGRESS",
                "assigned_to": "chandan.kumar"
            },
            {
                "request_id": "SR-202609-0009",
                "cif": "CIF100003",
                "customer_name": "Vikramaditya Rao",
                "request_type": "NRI_TAX_EXEMPTION_15CA",
                "details": {"nre_account": "101000005521", "assessment_year": "2026-27", "repatriation_usd": 50000},
                "submitted_at": "2026-09-04T12:00:00Z",
                "status": "APPROVED",
                "assigned_to": "tarun.chand"
            }
        ]

        # 16. Audit Logs (PRD 6.9 US-23)
        self.audit_logs = [
            {
                "log_id": "AUDIT-20260907-0091",
                "timestamp": "2026-09-07T05:45:12Z",
                "admin_user": "rajesh.amin",
                "action_type": "CIF_STATUS_UPDATE",
                "target_resource_id": "CIF100001",
                "ip_address": "10.20.4.115",
                "old_value": {"digital_status": "PENDING_VERIFICATION"},
                "new_value": {"digital_status": "ACTIVE"},
                "status": "SUCCESS"
            },
            {
                "log_id": "AUDIT-20260906-0082",
                "timestamp": "2026-09-06T14:10:00Z",
                "admin_user": "tarun.chand",
                "action_type": "AUTH_RULE_MODIFIED",
                "target_resource_id": "RULE-CORP-TXN-01",
                "ip_address": "10.20.4.118",
                "old_value": {"max_amount": 500000.00},
                "new_value": {"max_amount": 1000000.00},
                "status": "SUCCESS"
            },
            {
                "log_id": "AUDIT-20260906-0078",
                "timestamp": "2026-09-06T11:30:20Z",
                "admin_user": "priya.sharma",
                "action_type": "SERVICE_REQUEST_APPROVE",
                "target_resource_id": "SR-202609-0011",
                "ip_address": "10.20.4.116",
                "old_value": {"status": "PENDING"},
                "new_value": {"status": "COMPLETED"},
                "status": "SUCCESS"
            },
            {
                "log_id": "AUDIT-20260905-0065",
                "timestamp": "2026-09-05T16:00:00Z",
                "admin_user": "rajesh.amin",
                "action_type": "DYNAMIC_THEME_UPDATE",
                "target_resource_id": "bharat_bank_modern_v1",
                "ip_address": "10.20.4.115",
                "old_value": {"theme_version": "1.1.0"},
                "new_value": {"theme_version": "1.2.0"},
                "status": "SUCCESS"
            }
        ]

        # 17. Scheduled Transfers & Standing Instructions
        self.scheduled_transfers = [
            {
                "schedule_id": "SCH-001",
                "cif": "CIF100001",
                "debit_account_number": "101000000012",
                "beneficiary_name": "Sneha Mehta",
                "beneficiary_account_number": "99182390129182",
                "beneficiary_ifsc": "BCOB0001234",
                "amount": 25000.00,
                "frequency": "MONTHLY",
                "next_execution_date": "2026-10-01",
                "transfer_type": "IMPS",
                "status": "ACTIVE"
            },
            {
                "schedule_id": "SCH-002",
                "cif": "CIF100001",
                "debit_account_number": "101000000012",
                "beneficiary_name": "Bharat Bluechip Flexi SIP",
                "beneficiary_account_number": "50200088997821",
                "beneficiary_ifsc": "HDFC0000999",
                "amount": 25000.00,
                "frequency": "MONTHLY",
                "next_execution_date": "2026-10-12",
                "transfer_type": "IMPS",
                "status": "ACTIVE"
            }
        ]

        # 18. Customer In-App Notifications
        self.notifications = [
            {
                "notification_id": "NOTIF-101",
                "cif": "CIF100001",
                "category": "TRANSACTION",
                "title": "Salary Credited",
                "message": "₹2,25,000.00 credited to account ending 0012 by Nexus Tech Enterprises.",
                "timestamp": "2026-09-07T04:30:00Z",
                "is_read": False,
                "action_url": "/accounts/101000000012/statement",
                "icon": "arrow_downward"
            },
            {
                "notification_id": "NOTIF-102",
                "cif": "CIF100001",
                "category": "BILL_DUE",
                "title": "Adani Electricity Bill Due",
                "message": "Bill amount of ₹4,500.00 is due on 20 Sep 2026. Pay now to avoid late fees.",
                "timestamp": "2026-09-06T10:15:00Z",
                "is_read": False,
                "action_url": "/bills/pay",
                "icon": "flash_on"
            },
            {
                "notification_id": "NOTIF-103",
                "cif": "CIF100001",
                "category": "SECURITY",
                "title": "New Device Login Detected",
                "message": "Login to Bharat Bank Mobile detected on iPhone 15 Pro Max at 09:42 AM.",
                "timestamp": "2026-09-05T09:42:00Z",
                "is_read": True,
                "action_url": "/profile/security",
                "icon": "security"
            },
            {
                "notification_id": "NOTIF-104",
                "cif": "CIF100001",
                "category": "OFFER",
                "title": "Special Monsoon FD Rates",
                "message": "Lock in guaranteed 7.75% p.a. on 444 Days Special Monsoon Fixed Deposit.",
                "timestamp": "2026-09-04T12:00:00Z",
                "is_read": True,
                "action_url": "/deposits/open-fd",
                "icon": "savings"
            }
        ]

        # 19. Registered Utility Billers (Saved in Customer Profile)
        self.registered_billers = [
            {
                "registered_biller_id": "REG-BLR-001",
                "cif": "CIF100001",
                "biller_id": "BLR-ADANI-MUM",
                "biller_name": "Adani Electricity Mumbai Limited",
                "category_id": "ELECTRICITY",
                "category_name": "Electricity",
                "consumer_number": "1029384756",
                "nickname": "Bandra Apartment Electricity",
                "auto_pay_enabled": False,
                "last_paid_amount": 4500.00,
                "last_paid_date": "2026-08-14",
                "created_at": "2025-06-10T10:00:00Z"
            },
            {
                "registered_biller_id": "REG-BLR-002",
                "cif": "CIF100001",
                "biller_id": "BLR-MAHAVITARAN",
                "biller_name": "MSEDCL (Mahavitaran)",
                "category_id": "ELECTRICITY",
                "category_name": "Electricity",
                "consumer_number": "991823019283",
                "nickname": "Pune Farmhouse Power",
                "auto_pay_enabled": False,
                "last_paid_amount": 1820.00,
                "last_paid_date": "2026-08-01",
                "created_at": "2025-08-15T11:20:00Z"
            },
            {
                "registered_biller_id": "REG-BLR-003",
                "cif": "CIF100001",
                "biller_id": "BLR-AIRTEL-FIBER",
                "biller_name": "Bharti Airtel Broadband",
                "category_id": "BROADBAND",
                "category_name": "Broadband & Landline",
                "consumer_number": "02226489102",
                "nickname": "Home Wi-Fi Gigabit",
                "auto_pay_enabled": True,
                "last_paid_amount": 1179.00,
                "last_paid_date": "2026-08-28",
                "created_at": "2025-09-01T14:30:00Z"
            }
        ]

        # 20. Scheduled & Recurring Utility Bill Payments
        self.scheduled_bills = [
            {
                "schedule_id": "SCH-BILL-001",
                "cif": "CIF100001",
                "biller_id": "BLR-ADANI-MUM",
                "biller_name": "Adani Electricity Mumbai Limited",
                "consumer_number": "1029384756",
                "debit_account_number": "101000000012",
                "amount": 4500.00,
                "formatted_amount": "₹4,500.00",
                "scheduled_date": "2026-09-18",
                "notes": "Scheduled before due date",
                "status": "SCHEDULED",
                "created_at": "2026-09-07T08:00:00Z"
            }
        ]

        self.recurring_bills = [
            {
                "mandate_id": "REC-BILL-001",
                "cif": "CIF100001",
                "biller_id": "BLR-AIRTEL-FIBER",
                "biller_name": "Bharti Airtel Broadband",
                "consumer_number": "02226489102",
                "debit_account_number": "101000000012",
                "max_auto_pay_amount": 2000.00,
                "formatted_max_amount": "₹2,000.00",
                "frequency": "MONTHLY",
                "start_date": "2026-09-01",
                "end_date": "2027-09-01",
                "status": "ACTIVE",
                "next_due_date": "2026-09-28"
            }
        ]

        # 21. Bill Payment Transactions Store (with final status)
        self.bill_transactions = {
            "BBPS-20260907-001": {
                "transaction_id": "BBPS-20260907-001",
                "bbps_reference_no": "BBPS99102830182",
                "biller_id": "BLR-ADANI-MUM",
                "biller_name": "Adani Electricity Mumbai Limited",
                "consumer_number": "1029384756",
                "amount": 4500.00,
                "formatted_amount": "₹4,500.00",
                "payment_status": "SUCCESS",
                "payment_timestamp": "2026-09-07T09:30:00Z",
                "payment_mode": "BBPS_DEBIT",
                "debit_account_number": "101000000012",
                "npci_txn_ref": "NPCI20260907100029",
                "receipt_url": "https://bbps.bharatbank.com/receipts/BBPS-20260907-001.pdf"
            },
            "BBPS-20260904-002": {
                "transaction_id": "BBPS-20260904-002",
                "bbps_reference_no": "BBPS88192039101",
                "biller_id": "BLR-AIRTEL-FIBER",
                "biller_name": "Bharti Airtel Broadband",
                "consumer_number": "02226489102",
                "amount": 1179.00,
                "formatted_amount": "₹1,179.00",
                "payment_status": "SUCCESS",
                "payment_timestamp": "2026-09-04T14:20:00Z",
                "payment_mode": "BBPS_DEBIT",
                "debit_account_number": "101000000012",
                "npci_txn_ref": "NPCI20260904142011",
                "receipt_url": "https://bbps.bharatbank.com/receipts/BBPS-20260904-002.pdf"
            }
        }


# Singleton instance
mock_db = MockDataStore()

# Expand Mock Data Store with CBS Backoffice entities
def enrich_cbs_admin_mock_data(store):
    # 18. Account Liens
    store.account_liens = [
        {
            "lien_id": "LIEN-001",
            "account_number": "101000000012",
            "lien_amount": 2000.00,
            "reason": "COLLATERAL_HOLD",
            "marked_by": "rajesh.amin",
            "marked_at": "2026-09-01T10:00:00Z",
            "status": "ACTIVE"
        }
    ]

    # 19. Loan Origination / RPM Applications (Mirrors CBS v3 Process Driver)
    store.loan_applications = [
        {
            "application_no": "APP202609040001",
            "process_ref_no": "PRC99881122",
            "cif": "CIF100001",
            "customer_name": "Arjun Mehta",
            "mobile_number": "9876543210",
            "product_type": "LOAN",
            "product_sub_type": "HOME_LOAN",
            "business_product_name": "Prime Home Loan",
            "requested_amount": 3000000.00,
            "tenure_months": 180,
            "interest_rate": 8.50,
            "channel": "OBDX",
            "status": "UNDER_REVIEW",
            "applied_date": "2026-09-04",
            "risk_score": 780,
            "documents": [
                {
                    "document_id": "DOC001",
                    "document_name": "Identity Proof (Aadhaar / Passport)",
                    "document_type": "KYC",
                    "mandatory": True,
                    "status": "VERIFIED",
                    "file_url": "https://docs.bharatbank.com/rpm/doc001.pdf",
                    "verified_by": "priya.sharma"
                },
                {
                    "document_id": "DOC002",
                    "document_name": "Salary Slips (Last 3 Months)",
                    "document_type": "INCOME_PROOF",
                    "mandatory": True,
                    "status": "VERIFIED",
                    "file_url": "https://docs.bharatbank.com/rpm/doc002.pdf",
                    "verified_by": "priya.sharma"
                },
                {
                    "document_id": "DOC003",
                    "document_name": "Property Sale Agreement & NOC",
                    "document_type": "COLLATERAL",
                    "mandatory": True,
                    "status": "PENDING",
                    "file_url": "https://docs.bharatbank.com/rpm/doc003.pdf",
                    "verified_by": None
                }
            ]
        },
        {
            "application_no": "APP202609050002",
            "process_ref_no": "PRC99881125",
            "cif": "CIF100002",
            "customer_name": "Sneha Mehta",
            "mobile_number": "9876543211",
            "product_type": "LOAN",
            "product_sub_type": "AUTO_LOAN",
            "business_product_name": "DriveEasy Car Loan",
            "requested_amount": 800000.00,
            "tenure_months": 60,
            "interest_rate": 8.90,
            "channel": "MOBILE",
            "status": "SANCTIONED",
            "applied_date": "2026-09-05",
            "risk_score": 810,
            "documents": [
                {
                    "document_id": "DOC101",
                    "document_name": "Aadhaar Card",
                    "document_type": "KYC",
                    "mandatory": True,
                    "status": "VERIFIED",
                    "file_url": "https://docs.bharatbank.com/rpm/doc101.pdf",
                    "verified_by": "priya.sharma"
                }
            ]
        }
    ]

    # 20. Inward CTS Cheque Clearing Queue (Mirrors CBS v3 Cheque Clearing)
    store.inward_cheques = [
        {
            "cheque_id": "CTS-CLR-0091",
            "cheque_number": "100001",
            "drawer_account_number": "101000000012",
            "drawer_name": "Arjun Mehta",
            "presenting_bank_ifsc": "HDFC0000456",
            "presenting_bank_name": "HDFC Bank",
            "amount": 5000.00,
            "clearing_cycle": "CTS GRID 1",
            "clearing_date": "2026-09-07",
            "status": "PENDING",
            "cheque_image_front": "https://cts.bharatbank.com/cheques/100001_front.jpg",
            "cheque_image_back": "https://cts.bharatbank.com/cheques/100001_back.jpg"
        },
        {
            "cheque_id": "CTS-CLR-0092",
            "cheque_number": "550001",
            "drawer_account_number": "101000009943",
            "drawer_name": "Arjun Mehta",
            "presenting_bank_ifsc": "ICIC0000108",
            "presenting_bank_name": "ICICI Bank",
            "amount": 25000.00,
            "clearing_cycle": "CTS GRID 2",
            "clearing_date": "2026-09-07",
            "status": "PENDING",
            "cheque_image_front": "https://cts.bharatbank.com/cheques/550001_front.jpg",
            "cheque_image_back": "https://cts.bharatbank.com/cheques/550001_back.jpg"
        }
    ]

    # 21. Cheque Book Inventory by Branch
    store.cheque_inventory = [
        {
            "branch_code": "001",
            "branch_name": "Nariman Point Branch",
            "stock_25_leaves": 140,
            "stock_50_leaves": 95,
            "stock_100_leaves": 50,
            "last_replenished_on": "2026-08-28"
        },
        {
            "branch_code": "002",
            "branch_name": "BKC Metro Branch",
            "stock_25_leaves": 210,
            "stock_50_leaves": 150,
            "stock_100_leaves": 80,
            "last_replenished_on": "2026-09-01"
        }
    ]

    # 22. Branch Master Directory
    store.branches = [
        {
            "branch_code": "001",
            "branch_name": "Nariman Point Branch",
            "ifsc": "APEX0001048",
            "micr": "400002001",
            "city": "Mumbai",
            "branch_manager": "Deepak Verma",
            "cash_in_vault": 12500000.00,
            "lockers_total": 250,
            "lockers_occupied": 215,
            "is_active": True
        },
        {
            "branch_code": "002",
            "branch_name": "BKC Metro Branch",
            "ifsc": "APEX0001002",
            "micr": "400002002",
            "city": "Mumbai",
            "branch_manager": "Sunil Nair",
            "cash_in_vault": 25000000.00,
            "lockers_total": 400,
            "lockers_occupied": 360,
            "is_active": True
        },
        {
            "branch_code": "003",
            "branch_name": "Connaught Place Branch",
            "ifsc": "APEX0002001",
            "micr": "110002001",
            "city": "New Delhi",
            "branch_manager": "Anil Kapoor",
            "cash_in_vault": 18000000.00,
            "lockers_total": 300,
            "lockers_occupied": 270,
            "is_active": True
        }
    ]

    # 23. Locker Inventory (Mirrors CBS v3 locker_inquiry)
    store.lockers = [
        {
            "locker_id": "LCK-001-A12",
            "branch_code": "001",
            "locker_type": "SMALL",
            "annual_rent": 1500.00,
            "status": "AVAILABLE",
            "allotted_to_cif": None,
            "allotment_date": None
        },
        {
            "locker_id": "LCK-001-B05",
            "branch_code": "001",
            "locker_type": "MEDIUM",
            "annual_rent": 3000.00,
            "status": "OCCUPIED",
            "allotted_to_cif": "CIF100001",
            "allotment_date": "2024-05-10"
        },
        {
            "locker_id": "LCK-001-C01",
            "branch_code": "001",
            "locker_type": "LARGE",
            "annual_rent": 5000.00,
            "status": "AVAILABLE",
            "allotted_to_cif": None,
            "allotment_date": None
        },
        {
            "locker_id": "LCK-001-D01",
            "branch_code": "001",
            "locker_type": "EXTRA_LARGE",
            "annual_rent": 8000.00,
            "status": "OCCUPIED",
            "allotted_to_cif": "CIF-CORP-9001",
            "allotment_date": "2023-09-01"
        }
    ]

    # 24. Daily Reconciliation & Settlement Batches
    store.settlement_batches = [
        {
            "batch_id": "SETTLE-20260907-IMPS-01",
            "payment_rail": "IMPS",
            "settlement_cycle": "CYCLE_01 (00:00 - 06:00)",
            "total_txns": 1420,
            "total_volume": 18950000.00,
            "matched_txns": 1418,
            "unreconciled_txns": 2,
            "status": "DISCREPANCY",
            "reconciled_at": "2026-09-07T06:30:00Z"
        },
        {
            "batch_id": "SETTLE-20260906-NEFT-B2",
            "payment_rail": "NEFT",
            "settlement_cycle": "CYCLE_B2 (Hourly 15:00)",
            "total_txns": 850,
            "total_volume": 64200000.00,
            "matched_txns": 850,
            "unreconciled_txns": 0,
            "status": "RECONCILED",
            "reconciled_at": "2026-09-06T16:00:00Z"
        },
        {
            "batch_id": "SETTLE-20260906-RTGS-01",
            "payment_rail": "RTGS",
            "settlement_cycle": "EOD GROSS SETTLEMENT",
            "total_txns": 142,
            "total_volume": 125000000.00,
            "matched_txns": 142,
            "unreconciled_txns": 0,
            "status": "RECONCILED",
            "reconciled_at": "2026-09-06T19:30:00Z"
        }
    ]

    store.reconciliation_exceptions = [
        {
            "exception_id": "EXC-9912",
            "batch_id": "SETTLE-20260907-IMPS-01",
            "txn_ref": "TXN-20260907-88912",
            "utr": "UTR-IMPS-20260907-99120",
            "amount": 5000.00,
            "issue_type": "SWITCH_TIMEOUT",
            "resolution_status": "OPEN"
        },
        {
            "exception_id": "EXC-9913",
            "batch_id": "SETTLE-20260907-IMPS-01",
            "txn_ref": "TXN-20260907-77182",
            "utr": "UTR-IMPS-20260907-55192",
            "amount": 12500.00,
            "issue_type": "CBS_FAIL_NPCI_SUCCESS",
            "resolution_status": "OPEN"
        }
    ]

# Apply to mock_db
enrich_cbs_admin_mock_data(mock_db)
