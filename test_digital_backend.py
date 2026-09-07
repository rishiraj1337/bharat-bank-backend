
from fastapi.testclient import TestClient
from digital_backend.main import app

client = TestClient(app)

def test_system_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "UP"
    assert "flutter" in res.json()["collections"]
    assert "admin" in res.json()["collections"]

def test_swagger_specs():
    res_f = client.get("/openapi-flutter.json")
    assert res_f.status_code == 200
    assert "paths" in res_f.json()
    assert "/api/v1/app/dashboard" in res_f.json()["paths"]

    res_a = client.get("/openapi-admin.json")
    assert res_a.status_code == 200
    assert "paths" in res_a.json()
    assert "/api/v1/admin/customers" in res_a.json()["paths"]

    res_c = client.get("/openapi.json")
    assert res_c.status_code == 200
    assert len(res_c.json()["paths"]) >= len(res_f.json()["paths"])

def test_flutter_version_and_theme():
    # Version
    res = client.get("/api/v1/app/version")
    assert res.status_code == 200
    assert res.json()["data"]["app_version"] == "2.4.0"
    assert len(res.json()["data"]["subsystems"]) >= 4

    # Theme
    res = client.get("/api/v1/app/theme")
    assert res.status_code == 200
    theme = res.json()["data"]
    assert theme["is_dark_mode_configured"] is True
    assert "primary" in theme["light_colors"]
    assert "primary" in theme["dark_colors"]
    assert theme["logo_url"] is not None

def test_flutter_dashboard():
    res = client.get("/api/v1/app/dashboard")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["customer"]["name"] == "Arjun Mehta"
    assert data["customer"]["segment"] == "RETAIL"
    assert len(data["accounts"]) >= 2
    assert len(data["quick_actions"]) == 4
    assert len(data["banking_services"]) == 16
    assert len(data["credit_cards"]) >= 1
    assert data["credit_cards"][0]["total_outstanding_due"] == 67500.00
    assert len(data["recent_transactions"]) == 5
    assert len(data["pre_approved_offers"]) >= 1

def test_flutter_accounts_and_statements():
    # List Accounts
    res = client.get("/api/v1/app/accounts")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2

    # Account Detail
    res = client.get("/api/v1/app/accounts/101000000012")
    assert res.status_code == 200
    assert res.json()["data"]["account_type"] == "Savings Account"

    # Mini Statement
    res = client.get("/api/v1/app/accounts/101000000012/mini-statement")
    assert res.status_code == 200
    assert len(res.json()["data"]) == 5

    # Full Statement
    res = client.get("/api/v1/app/accounts/101000000012/statement?from_date=2026-08-01&to_date=2026-09-07")
    assert res.status_code == 200
    assert res.json()["data"]["total_records"] >= 5

    # Statement Download
    res = client.get("/api/v1/app/accounts/101000000012/statement/download?format=PDF")
    assert res.status_code == 200
    assert "download_url" in res.json()["data"]

    # Limits
    res = client.get("/api/v1/app/accounts/101000000012/limits")
    assert res.status_code == 200

def test_flutter_transfers_and_beneficiaries():
    # Transfer types
    res = client.get("/api/v1/app/transfers/transfer-types")
    assert res.status_code == 200
    assert len(res.json()["data"]) == 4

    # Beneficiaries list
    res = client.get("/api/v1/app/beneficiaries")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 5

    # Add Beneficiary
    res = client.post("/api/v1/app/beneficiaries", json={
        "name": "Kavita Sharma",
        "account_number": "102030405060",
        "confirm_account_number": "102030405060",
        "ifsc": "HDFC0000123",
        "bank_name": "HDFC Bank",
        "account_type": "SAVINGS"
    })
    assert res.status_code == 200
    assert res.json()["data"]["name"] == "Kavita Sharma"

    # Fund Transfer Initiate
    res = client.post("/api/v1/app/transfers/initiate", json={
        "debit_account_number": "101000000012",
        "beneficiary_name": "Sneha Mehta",
        "beneficiary_account_number": "99182390129182",
        "beneficiary_ifsc": "BCOB0001234",
        "amount": 5000.0,
        "transfer_type": "IMPS",
        "note": "Payment note"
    })
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "SUCCESS"
    assert res.json()["data"]["amount"] == 5000.0

def test_flutter_auth_and_verification():
    # MPIN verify success
    res = client.post("/api/v1/app/auth/mpin/verify", json={"mpin": "1234"})
    assert res.status_code == 200
    assert res.json()["data"]["cif"] == "CIF100001"

    # MPIN verify failure
    res = client.post("/api/v1/app/auth/mpin/verify", json={"mpin": "9999"})
    assert res.status_code == 400

    # Biometric verify
    res = client.post("/api/v1/app/auth/biometric/verify", json={
        "cif": "CIF100001",
        "biometric_token": "token_123",
        "device_id": "DEV-01"
    })
    assert res.status_code == 200

    # OTP Send & Verify
    res = client.post("/api/v1/app/auth/otp/send", json={"cif": "CIF100001", "purpose": "LOGIN"})
    assert res.status_code == 200
    ref = res.json()["data"]["otp_reference"]

    res_v = client.post("/api/v1/app/auth/otp/verify", json={"otp_reference": ref, "otp_code": "123456"})
    assert res_v.status_code == 200

def test_flutter_cards_deposits_loans():
    # Cards
    res = client.get("/api/v1/app/cards")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2

    # Lock toggle
    res = client.post("/api/v1/app/cards/CRD-3349/lock-toggle", json={"is_locked": True})
    assert res.status_code == 200

    # Deposits rates
    res = client.get("/api/v1/app/deposits/rates")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 5

    # Loans list
    res = client.get("/api/v1/app/loans")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 1

def test_admin_portal_endpoints():
    # Users
    res = client.get("/api/v1/admin/users")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 3

    # Customers
    res = client.get("/api/v1/admin/customers")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 3

    # Customer 360
    res = client.get("/api/v1/admin/customers/CIF100001")
    assert res.status_code == 200
    assert res.json()["data"]["cif"] == "CIF100001"
    assert len(res.json()["data"]["accounts"]) >= 2

    # Authorization Rules
    res = client.get("/api/v1/admin/auth-rules")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2

    # Corporate Hierarchies
    res = client.get("/api/v1/admin/auth-rules/corporate-hierarchies")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2

    # Operations Transactions
    res = client.get("/api/v1/admin/operations/transactions")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2

    # Service Requests
    res = client.get("/api/v1/admin/operations/service-requests")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2

    # Audit Logs
    res = client.get("/api/v1/admin/reports/audit-logs")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2

    # Export Report
    res = client.post("/api/v1/admin/reports/export", json={
        "report_type": "TRANSACTIONS",
        "from_date": "2026-08-01",
        "to_date": "2026-09-07",
        "format": "CSV"
    })
    assert res.status_code == 200
    assert "download_url" in res.json()["data"]

    # Dynamic Theme Admin Config
    res = client.get("/api/v1/admin/theme-config")
    assert res.status_code == 200
    assert res.json()["data"]["theme_id"] == "bharat_bank_modern_v1"

if __name__ == "__main__":
    test_system_health()
    test_swagger_specs()
    test_flutter_version_and_theme()
    test_flutter_dashboard()
    test_flutter_accounts_and_statements()
    test_flutter_transfers_and_beneficiaries()
    test_flutter_auth_and_verification()
    test_flutter_cards_deposits_loans()
    test_admin_portal_endpoints()
    print("ALL 9 COMPREHENSIVE INTEGRATION TESTS EXECUTED AND PASSED SUCCESSFULLY!")

def test_admin_cbs_backoffice_endpoints():
    # 1. CBS Accounts list & freeze/unfreeze
    res = client.get("/api/v1/admin/cbs-accounts")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 3

    # Freeze
    res = client.post("/api/v1/admin/cbs-accounts/101000000012/freeze", json={
        "freeze_type": "DEBIT",
        "reason_code": "KYC_PENDING"
    })
    assert res.status_code == 200

    # Unfreeze
    res = client.post("/api/v1/admin/cbs-accounts/101000000012/unfreeze", json={
        "reason_code": "KYC_VERIFIED"
    })
    assert res.status_code == 200

    # Liens
    res = client.get("/api/v1/admin/cbs-accounts/101000000012/liens")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 1

    # 2. Loan Underwriting & RPM
    res = client.get("/api/v1/admin/loans-underwriting/applications")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2
    app_no = res.json()["data"][0]["application_no"]

    res = client.get(f"/api/v1/admin/loans-underwriting/applications/{app_no}")
    assert res.status_code == 200
    assert "domain_applicant_data" in res.json()["data"]

    res = client.get(f"/api/v1/admin/loans-underwriting/applications/{app_no}/documents")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2

    # Decision
    res = client.post(f"/api/v1/admin/loans-underwriting/applications/{app_no}/decision", json={
        "decision": "APPROVE",
        "sanctioned_amount": 3000000.0,
        "sanctioned_interest_rate": 8.5,
        "remarks": "Approved with CIBIL 780"
    })
    assert res.status_code == 200

    # 3. CTS Cheque Clearing
    res = client.get("/api/v1/admin/cbs-cheques/inward-clearing")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2

    # Action cheque
    res = client.post("/api/v1/admin/cbs-cheques/inward-clearing/CTS-CLR-0091/action", json={
        "action": "CLEAR"
    })
    assert res.status_code == 200

    # Inventory
    res = client.get("/api/v1/admin/cbs-cheques/inventory")
    assert res.status_code == 200

    # 4. Branches & Lockers
    res = client.get("/api/v1/admin/cbs-branches-lockers/branches")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 3

    res = client.get("/api/v1/admin/cbs-branches-lockers/lockers?branch_code=001")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 4

    # Allot locker
    res = client.post("/api/v1/admin/cbs-branches-lockers/lockers/allot", json={
        "locker_id": "LCK-001-A12",
        "cif": "CIF100001",
        "debit_account_number": "101000000012"
    })
    assert res.status_code == 200

    # 5. TD Trial Pre-closure
    res = client.get("/api/v1/admin/cbs-deposits/FD-1010000091/trial-closure")
    assert res.status_code == 200
    assert res.json()["data"]["net_payable"] > 0

    # 6. Settlement & Reconciliation
    res = client.get("/api/v1/admin/cbs-reconciliation/batches")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 3

    res = client.post("/api/v1/admin/cbs-reconciliation/batches/SETTLE-20260907-IMPS-01/reconcile")
    assert res.status_code == 200

    res = client.get("/api/v1/admin/cbs-reconciliation/exceptions")
    assert res.status_code == 200
    assert len(res.json()["data"]) >= 2


def test_flutter_v2_superset_endpoints():
    # 1. Verify OpenAPI v2 Schema
    res_v2 = client.get("/openapi-flutter-v2.json")
    assert res_v2.status_code == 200
    paths = res_v2.json()["paths"]
    assert "/api/v2/app/auth/logout" in paths
    assert "/api/v2/app/profile" in paths
    assert "/api/v2/app/notifications" in paths
    assert "/api/v2/app/notifications/{notification_id}/read" in paths
    assert "/api/v2/app/deposits/open-rd" in paths
    assert "/api/v2/app/bills/schedule" in paths
    assert "/api/v2/app/bills/recurring" in paths
    assert "/api/v2/app/bills/registered-billers" in paths
    assert "/api/v2/app/bills/registered-billers/{registered_biller_id}" in paths
    assert "/api/v2/app/bills/{transaction_id}/status" in paths
    # Verify v1 superset inheritance
    assert "/api/v2/app/dashboard" in paths
    assert "/api/v2/app/accounts" in paths
    assert "/api/v2/app/transfers/initiate" in paths

    # 2. Logout - POST /api/v2/app/auth/logout
    res = client.post("/api/v2/app/auth/logout", headers={"Authorization": "Bearer mock_test_token"})
    assert res.status_code == 200
    assert res.json()["success"] is True
    assert "logged out" in res.json()["message"].lower()

    # 3. Profile - GET /api/v2/app/profile
    res = client.get("/api/v2/app/profile?cif=CIF100001")
    assert res.status_code == 200
    prof = res.json()["data"]
    assert prof["cif"] == "CIF100001"
    assert prof["full_name"] == "Arjun Mehta"
    assert prof["kyc_status"] == "VERIFIED"
    assert prof["registered_accounts_count"] >= 2
    assert "email_alerts" in prof["communication_preferences"]

    # 4. Notifications - GET /api/v2/app/notifications
    res = client.get("/api/v2/app/notifications?cif=CIF100001")
    assert res.status_code == 200
    notifs = res.json()["data"]
    assert len(notifs) >= 3
    first_notif_id = notifs[0]["notification_id"]

    # 5. Notifications/{id}/read - PUT /api/v2/app/notifications/{id}/read
    res = client.put(f"/api/v2/app/notifications/{first_notif_id}/read")
    assert res.status_code == 200
    assert res.json()["success"] is True

    # 6. Open-RD - POST /api/v2/app/deposits/open-rd
    res = client.post("/api/v2/app/deposits/open-rd", json={
        "debit_account_number": "101000000012",
        "monthly_installment_amount": 5000.00,
        "tenure_months": 12,
        "installment_day": 5,
        "auto_debit": True,
        "nominee_name": "Sneha Mehta"
    })
    assert res.status_code == 200
    rd_data = res.json()["data"]
    assert rd_data["deposit_type"] == "RECURRING_DEPOSIT"
    assert rd_data["principal_amount"] == 5000.00
    assert rd_data["maturity_amount"] > 60000.00

    # 7. Bill Schedule - POST /api/v2/app/bills/schedule
    res = client.post("/api/v2/app/bills/schedule", json={
        "biller_id": "BLR-ADANI-MUM",
        "biller_name": "Adani Electricity Mumbai Limited",
        "consumer_number": "1029384756",
        "debit_account_number": "101000000012",
        "amount": 4500.00,
        "scheduled_date": "2026-09-18",
        "notes": "Electricity bill test schedule"
    })
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "SCHEDULED"

    # 8. Bill Recurring - POST /api/v2/app/bills/recurring
    res = client.post("/api/v2/app/bills/recurring", json={
        "biller_id": "BLR-AIRTEL-FIBER",
        "biller_name": "Bharti Airtel Broadband",
        "consumer_number": "02226489102",
        "debit_account_number": "101000000012",
        "max_auto_pay_amount": 2500.00,
        "frequency": "MONTHLY",
        "start_date": "2026-09-01",
        "end_date": "2027-09-01"
    })
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "ACTIVE"

    # 9. Registered-billers - GET /api/v2/app/bills/registered-billers
    res = client.get("/api/v2/app/bills/registered-billers?cif=CIF100001")
    assert res.status_code == 200
    billers = res.json()["data"]
    assert len(billers) >= 2
    biller_to_del = billers[0]["registered_biller_id"]

    # 10. Registered-billers/{id} - DELETE /api/v2/app/bills/registered-billers/{id}
    res = client.delete(f"/api/v2/app/bills/registered-billers/{biller_to_del}")
    assert res.status_code == 200
    assert res.json()["success"] is True

    # 11. Bill status - GET /api/v2/app/bills/{transaction_id}/status
    res = client.get("/api/v2/app/bills/BBPS-20260907-001/status")
    assert res.status_code == 200
    status_data = res.json()["data"]
    assert status_data["transaction_id"] == "BBPS-20260907-001"
    assert status_data["payment_status"] == "SUCCESS"
    assert status_data["amount"] == 4500.00

    # 12. Superset Verification: V1 APIs via /api/v2/app/
    res = client.get("/api/v2/app/dashboard")
    assert res.status_code == 200
    assert res.json()["data"]["customer"]["name"] == "Arjun Mehta"

    res = client.get("/api/v2/app/accounts")
    assert res.status_code == 200

    res = client.get("/api/v2/app/version")
    assert res.status_code == 200

    # 13. Ensure V1 APIs continue to work at /api/v1/app/
    res = client.get("/api/v1/app/version")
    assert res.status_code == 200
    res = client.get("/api/v1/app/dashboard")
    assert res.status_code == 200


if __name__ == "__main__":
    test_admin_cbs_backoffice_endpoints()
    print("ALL CBS BACKOFFICE ADMIN INTEGRATION TESTS EXECUTED AND PASSED SUCCESSFULLY!")
    test_flutter_v2_superset_endpoints()
    print("ALL FLUTTER V2 SUPERSET INTEGRATION TESTS EXECUTED AND PASSED SUCCESSFULLY!")
