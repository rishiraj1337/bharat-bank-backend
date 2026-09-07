import unittest
from starlette.testclient import TestClient
from app.main import app

class TestCBSMockServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "UP")
        self.assertEqual(response.json()["versions"], ["v1", "v2", "v3"])

    # --- v1 Tests ---
    def test_v1_customer_account_inquiry(self):
        resp = self.client.post("/api/v1/customers/accounts/inquiry", json={"CustomerId": "CIF100001"}, headers={"Accept": "application/json"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["Customer"]["CustomerId"], "CIF100001")

    # --- v2 Tests ---
    def test_v2_business_products(self):
        resp = self.client.get("/api/v2/products/businessproducts?productType=LOAN", headers={"Accept": "application/json"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("data", resp.json())

    # --- v3 Tests (Unified Collection) ---
    def test_v3_customer_account_inquiry(self):
        # XML output
        resp_xml = self.client.post(
            "/api/v3/customers/accounts/inquiry",
            json={"CustomerId": "CIF100001"},
            headers={"Accept": "application/xml"}
        )
        self.assertEqual(resp_xml.status_code, 200)
        self.assertIn("<CustomerId>CIF100001</CustomerId>", resp_xml.text)
        self.assertIn("<IFSC>OBDX0000001</IFSC>", resp_xml.text)

        # JSON output
        resp_json = self.client.post(
            "/api/v3/customers/accounts/inquiry",
            json={"CustomerId": "CIF100001"},
            headers={"Accept": "application/json"}
        )
        self.assertEqual(resp_json.status_code, 200)
        data = resp_json.json()
        self.assertEqual(data["Customer"]["CustomerId"], "CIF100001")
        first_acc = data["Accounts"]["Account"][0]
        self.assertEqual(first_acc["AccountNumber"], "101000000001")
        self.assertEqual(first_acc["IFSC"], "OBDX0000001")
        self.assertIn("LienAmount", first_acc)

    def test_v3_account_statements(self):
        resp = self.client.post(
            "/api/v3/accounts/statements",
            json={"AccountId": "101000000001", "FromDate": "2026-08-01", "ToDate": "2026-09-04"},
            headers={"Accept": "application/json"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["AccountId"], "101000000001")
        self.assertIn("Transactions", data)

    def test_v3_loans_management(self):
        # Inquiry
        resp = self.client.post(
            "/api/v3/loans/inquiry",
            json={"CustomerId": "CIF100001"},
            headers={"Accept": "application/json"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Loans", resp.json())

        # Schedule
        resp_sched = self.client.post(
            "/api/v3/loans/schedule",
            json={"LoanAccountNumber": "LN1010000001"},
            headers={"Accept": "application/json"}
        )
        self.assertEqual(resp_sched.status_code, 200)
        self.assertIn("Schedule", resp_sched.json())

    def test_v3_term_deposits(self):
        # Inquiry
        resp = self.client.post(
            "/api/v3/deposits/td/inquiry",
            json={"CustomerId": "CIF100001"},
            headers={"Accept": "application/json"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Deposits", resp.json())

        # Open
        resp_open = self.client.post(
            "/api/v3/deposits/td/open",
            json={"CustomerId": "CIF100001", "DebitAccountNumber": "101000000001", "Amount": 100000.0, "TenureMonths": 12},
            headers={"Accept": "application/json"}
        )
        self.assertEqual(resp_open.status_code, 201)
        self.assertEqual(resp_open.json()["Status"], "ACTIVE")

    def test_v3_fund_transfer(self):
        resp = self.client.post(
            "/api/v3/payments/transfer",
            json={
                "DebtorAccount": "101000000001",
                "CreditorAccount": "202000000002",
                "BeneficiaryName": "Jane Doe",
                "Amount": 5000.0,
                "PaymentMode": "IMPS"
            },
            headers={"Accept": "application/json"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["Status"], "SUCCESS")

    def test_v3_rpm_origination(self):
        # Products
        resp_prod = self.client.post(
            "/api/v3/products/businessproducts",
            json={"productType": "LOAN", "channel": "OBDX"},
            headers={"Accept": "application/json"}
        )
        self.assertEqual(resp_prod.status_code, 200)
        self.assertIn("data", resp_prod.json())

        # Initiate
        resp_init = self.client.post(
            "/api/v3/process/initiate",
            json={"productType": "LOAN", "channel": "OBDX", "custName": "John Doe"},
            headers={"Accept": "application/json"}
        )
        self.assertEqual(resp_init.status_code, 201)
        self.assertEqual(resp_init.json()["status"], "INITIATED")

    def test_openapi_schemas(self):
        resp_v1 = self.client.get("/openapi-v1.json")
        self.assertEqual(resp_v1.status_code, 200)
        self.assertIn("/api/v1/customers/accounts/inquiry", resp_v1.json()["paths"])

        resp_v2 = self.client.get("/openapi-v2.json")
        self.assertEqual(resp_v2.status_code, 200)
        self.assertIn("/api/v2/products/businessproducts", resp_v2.json()["paths"])

        resp_v3 = self.client.get("/openapi-v3.json")
        self.assertEqual(resp_v3.status_code, 200)
        self.assertIn("/api/v3/customers/accounts/inquiry", resp_v3.json()["paths"])
        self.assertIn("/api/v3/accounts/statements", resp_v3.json()["paths"])
        self.assertIn("/api/v3/loans/inquiry", resp_v3.json()["paths"])

if __name__ == "__main__":
    unittest.main()
