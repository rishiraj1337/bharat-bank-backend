from typing import Dict, Any, Optional
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html

from digital_backend.config import settings
from digital_backend.logger import RequestResponseLoggingMiddleware, logger

# Import Flutter App Routers
from digital_backend.routers.flutter import system as flutter_system
from digital_backend.routers.flutter import auth as flutter_auth
from digital_backend.routers.flutter import dashboard as flutter_dashboard
from digital_backend.routers.flutter import accounts as flutter_accounts
from digital_backend.routers.flutter import transfers as flutter_transfers
from digital_backend.routers.flutter import beneficiaries as flutter_beneficiaries
from digital_backend.routers.flutter import cards as flutter_cards
from digital_backend.routers.flutter import deposits as flutter_deposits
from digital_backend.routers.flutter import loans as flutter_loans
from digital_backend.routers.flutter import bill_payments as flutter_bill_payments
from digital_backend.routers.flutter import cheques as flutter_cheques
from digital_backend.routers.flutter import services as flutter_services

# Import React Admin Routers
from digital_backend.routers.admin import users as admin_users
from digital_backend.routers.admin import customer_management as admin_customer_mgmt
from digital_backend.routers.admin import auth_rules as admin_auth_rules
from digital_backend.routers.admin import operations as admin_operations
from digital_backend.routers.admin import reports as admin_reports
from digital_backend.routers.admin import theme_config as admin_theme_config
from digital_backend.routers.admin import cbs_accounts as admin_cbs_accounts
from digital_backend.routers.admin import cbs_loans as admin_cbs_loans
from digital_backend.routers.admin import cbs_cheques as admin_cbs_cheques
from digital_backend.routers.admin import cbs_lockers as admin_cbs_lockers
from digital_backend.routers.admin import cbs_reconciliation as admin_cbs_reconciliation
from digital_backend.routers.admin import cbs_deposits as admin_cbs_deposits

app = FastAPI(
    title="Bharat Bank Omnichannel Digital Banking Backend",
    description="""
### Unified Digital Banking Backend API Platform
Detached microservices backend serving:
1. **Flutter Mobile Application** (Retail & Corporate Customer Experience)
2. **React Admin Console** (Branch Staff, Operations, Compliance, CBS Backoffice & Risk Management)

---

### Use the **Definition Dropdown** in the top navigation bar to switch between:
1. **`1. Flutter Mobile App (Customer Experience APIs)`**: Versioning, Dynamic Theming, Composite Dashboard, Accounts 360, Transfers (Within Bank, IMPS, NEFT, RTGS), Beneficiaries, Cards, Deposits, Loans, BBPS Utility Payments, Cheques, and Digital Services.
2. **`2. React Admin Console (Operations, Compliance & CBS Backoffice)`**: Admin Staff User/Role Management (US-20), Customer & CIF Linkage (US-21), Payment Authorization Matrix & Corporate Hierarchies (US-22), Live Switch Transaction Operations, Customer Service Request Management, CBS Account Servicing (Freeze, Unfreeze, Liens), Loan Underwriting & RPM Origination, Inward CTS Cheque Clearing, Branch & Locker Management, Daily Settlement & Reconciliation, Dynamic App Theme Studio, and Audit Reports (US-23).
3. **`All Digital Banking APIs (Combined)`**: Unified catalog of all customer and administrative endpoints.
""",
    version="1.0.0",
    docs_url=None,  # Handled by custom multi-collection Swagger UI below
    redoc_url="/redoc"
)

# Open CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Request-Response Logging Middleware
app.add_middleware(RequestResponseLoggingMiddleware)

# ==========================================================
# Group Routers into Dedicated Collections
# ==========================================================

# 1. Flutter Mobile App Master Router
flutter_master_router = APIRouter(prefix="/api/v1/app")
flutter_master_router.include_router(flutter_system.router)
flutter_master_router.include_router(flutter_auth.router)
flutter_master_router.include_router(flutter_dashboard.router)
flutter_master_router.include_router(flutter_accounts.router)
flutter_master_router.include_router(flutter_transfers.router)
flutter_master_router.include_router(flutter_beneficiaries.router)
flutter_master_router.include_router(flutter_cards.router)
flutter_master_router.include_router(flutter_deposits.router)
flutter_master_router.include_router(flutter_loans.router)
flutter_master_router.include_router(flutter_bill_payments.router)
flutter_master_router.include_router(flutter_cheques.router)
flutter_master_router.include_router(flutter_services.router)

# 2. React Admin Portal Master Router (Core Admin + CBS Integration Proxies)
admin_master_router = APIRouter(prefix="/api/v1/admin")
admin_master_router.include_router(admin_users.router)
admin_master_router.include_router(admin_customer_mgmt.router)
admin_master_router.include_router(admin_auth_rules.router)
admin_master_router.include_router(admin_operations.router)
admin_master_router.include_router(admin_cbs_accounts.router)
admin_master_router.include_router(admin_cbs_loans.router)
admin_master_router.include_router(admin_cbs_cheques.router)
admin_master_router.include_router(admin_cbs_lockers.router)
admin_master_router.include_router(admin_cbs_deposits.router)
admin_master_router.include_router(admin_cbs_reconciliation.router)
admin_master_router.include_router(admin_reports.router)
admin_master_router.include_router(admin_theme_config.router)

# Mount Routers onto FastAPI App
app.include_router(flutter_master_router)
app.include_router(admin_master_router)

# ==========================================================
# OpenAPI Schemas Cache & Generation
# ==========================================================
_openapi_flutter_cache: Optional[Dict[str, Any]] = None
_openapi_admin_cache: Optional[Dict[str, Any]] = None


@app.get("/openapi-flutter.json", include_in_schema=False)
async def get_openapi_flutter():
    global _openapi_flutter_cache
    if _openapi_flutter_cache is None:
        _openapi_flutter_cache = get_openapi(
            title="Bharat Bank Mobile App - Flutter Collection",
            version="1.0.0",
            description="""
### Collection 1: Flutter Mobile Banking Application APIs
- **System & Dynamics:** `/version` health & versioning, `/theme` dynamic light/dark colors and typography.
- **Authentication & Security:** MPIN verify/set, Biometric login, OTP verification, Registration & Password recovery.
- **Dashboard:** Composite `/dashboard` endpoint serving accounts, quick actions, 16 banking service modules, credit card widgets, recent transactions, and pre-approved loan offers.
- **Accounts & Statements:** 360 account details, Mini statements, Full PDF/Excel statements, Spending limits, and Uncleared funds.
- **Fund Transfers:** Within Bank, IMPS, NEFT, RTGS, Quick transfers, Scheduled recurring payments, and IFSC lookup.
- **Beneficiaries:** Payee directory with cooling-period enforcement and NPCI penny-drop validation.
- **Cards Management:** Signature Mastercard & RuPay Platinum Debit card controls, instant lock/unlock, blocking, and bill payment.
- **Term Deposits & Loans:** Online FD/RD creation, maturity calculator, deposit advice, loan portfolio, and amortization schedules.
- **BBPS & Utilities:** Utility bill fetching and payments, mobile recharges, and biller management.
- **Cheques & Services:** Cheque book requests, stop cheque, nominee management, and shareable IFSC cards.
""",
            routes=flutter_master_router.routes
        )
    return _openapi_flutter_cache


@app.get("/openapi-admin.json", include_in_schema=False)
async def get_openapi_admin():
    global _openapi_admin_cache
    if _openapi_admin_cache is None:
        _openapi_admin_cache = get_openapi(
            title="Bharat Bank Admin Console - React & CBS Collection",
            version="1.0.0",
            description="""
### Collection 2: React Admin Console & CBS Backoffice Operations APIs
- **Admin Users & Roles (US-20):** RBAC user management, roles, and granular security permissions.
- **Customer & CIF Operations (US-21, US-02):** Customer search, 360 profile, branch-assisted digital onboarding, CIF linking/unlinking, and KYC status updates.
- **CBS Account Controls:** List CBS accounts, Freeze (DEBIT/CREDIT/TOTAL), Unfreeze, Mark Liens, Release Liens, and Manual Ledger Adjustments.
- **Loan Underwriting & RPM Origination:** Oracle OBDX/RPM application inquiry, document checklist verification, sanction letter decisioning, and CBS disbursement triggers.
- **Cheque Clearing & CTS House:** Inward CTS clearing batch authorization, cheque return with RBI reason codes, and branch cheque book inventory.
- **Branches & Safe Deposit Lockers:** CBS branch master directory, vault cash holding, and locker allotment matrix (SMALL, MEDIUM, LARGE, EXTRA_LARGE).
- **Term Deposits & Pre-closure:** All deposits portfolio, TD pre-closure trial calculation, and premature settlement.
- **Settlement & Reconciliation:** Daily clearing cycles (IMPS/NEFT/RTGS/BBPS), NPCI 3-way reconciliation, and discrepancy resolution.
- **Authorization Rules (US-22):** Corporate payment maker-checker matrices, approval thresholds, tiers, and corporate hierarchies.
- **Real-Time Operations:** Live switch transaction stream monitoring, status override intervention with audit, and customer service request processing.
- **Reports & Audit Trail (US-23):** Immutable administrative audit trail, customer analytics, and multi-format report exports (CSV, Excel, PDF).
- **Dynamic App Theming:** Live branding and mobile app theme styling controls.
""",
            routes=admin_master_router.routes
        )
    return _openapi_admin_cache


# ==========================================================
# Custom Multi-Collection Swagger UI Handler
# ==========================================================

@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def custom_swagger_ui_html():
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <title>Bharat Bank Digital Banking API - Swagger UI</title>
    <style>
        html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
        *, *:before, *:after { box-sizing: inherit; }
        body { margin: 0; background: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .swagger-ui .topbar {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
            padding: 12px 24px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        .swagger-ui .topbar .download-url-wrapper {
            display: flex;
            align-items: center;
        }
        .swagger-ui .topbar select {
            background: #ffffff !important;
            color: #0f172a !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            font-size: 14px !important;
            border: 2px solid #3b82f6 !important;
            font-weight: 700 !important;
            cursor: pointer !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
            outline: none;
        }
        .swagger-ui .topbar select:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.4);
        }
        .swagger-ui .info .title {
            color: #1e3a8a;
            font-weight: 800;
        }
        .swagger-ui .opblock.opblock-post {
            border-color: #3b82f6;
            background: rgba(59, 130, 246, 0.05);
        }
        .swagger-ui .opblock.opblock-get {
            border-color: #10b981;
            background: rgba(16, 185, 129, 0.05);
        }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
    <script>
    window.onload = function() {
        window.ui = SwaggerUIBundle({
            urls: [
                {
                    name: "1. Flutter Mobile App (Customer Experience APIs)",
                    url: "/openapi-flutter.json"
                },
                {
                    name: "2. React Admin Console (Operations & CBS Backoffice)",
                    url: "/openapi-admin.json"
                },
                {
                    name: "3. All Digital Banking APIs (Combined)",
                    url: "/openapi.json"
                }
            ],
            "urls.primaryName": "1. Flutter Mobile App (Customer Experience APIs)",
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout",
            displayRequestDuration: true,
            filter: true,
            showExtensions: true,
            showCommonExtensions: true
        });
    };
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)


@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/health", tags=["System Health"])
async def health_check():
    return {
        "status": "UP",
        "service": settings.app_name,
        "version": settings.version,
        "collections": ["flutter", "admin"]
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.app_name} on {settings.host}:{settings.port}...")
    uvicorn.run("digital_backend.main:app", host=settings.host, port=settings.port, reload=True)
