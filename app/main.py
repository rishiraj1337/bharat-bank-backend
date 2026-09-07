from typing import Dict, Any, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from app.logger import RequestResponseLoggingMiddleware, logger
from app.routes import router as router_v1
from app.routes_v2 import router_v2
from app.routes_v3 import router_v3

app = FastAPI(
    title="Oracle FLEXCUBE & OBDX/RPM Unified Banking Mock API",
    description="""
### Unified Mock Server for Oracle FLEXCUBE Core Banking (CBS) and OBDX / RPM Digital Banking

---

### Use the **Definition Dropdown** in the top navigation bar to switch between:
1. **`v3 - Unified FLEXCUBE & Digital Banking (Recommended)`**: Combined synthesis of v1 & v2 with symmetric POST endpoint contracts, enriched schemas (IFSC, Lien, Nominees, Cards), XML/JSON envelopes, Statements, Loan Schedules, Term Deposits, and RPM Origination.
2. **`v1 - Core Banking System (CBS)`**: 20 canonical CBS / FLEXCUBE legacy integration endpoints.
3. **`v2 - OBDX / RPM & Digital Banking`**: Oracle OBDX/RPM Process Driver & Next-Gen Banking services.
4. **`All APIs (Combined)`**: Unified catalog of all available banking operations.
""",
    version="3.0.0",
    docs_url=None,  # Custom Swagger UI handler below
    redoc_url="/redoc"
)

# Open CORS middleware to serve clients from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Custom Request-Response Logging Middleware
app.add_middleware(RequestResponseLoggingMiddleware)

# Mount Routers
app.include_router(router_v1)
app.include_router(router_v2)
app.include_router(router_v3)

# Cached OpenAPI schemas
_openapi_v1_cache: Optional[Dict[str, Any]] = None
_openapi_v2_cache: Optional[Dict[str, Any]] = None
_openapi_v3_cache: Optional[Dict[str, Any]] = None


@app.get("/openapi-v1.json", include_in_schema=False)
async def get_openapi_v1():
    global _openapi_v1_cache
    if _openapi_v1_cache is None:
        _openapi_v1_cache = get_openapi(
            title="Core Banking System (CBS) - Collection v1",
            version="1.0.0",
            description="""
### Collection v1: Core Banking System (CBS) / FLEXCUBE Integration APIs
- Canonical CBS operations: Customer Account Inquiries, Account Freeze/Unfreeze, Cards, Cheques (Issued, Deposited, Leaves), Certificates (Interest, TDS), Lockers, TD Trial Closure.
- Envelopes: `<CBSRequest>` & `<CBSResponse>` (XML) or JSON.
""",
            routes=router_v1.routes
        )
    return _openapi_v1_cache


@app.get("/openapi-v2.json", include_in_schema=False)
async def get_openapi_v2():
    global _openapi_v2_cache
    if _openapi_v2_cache is None:
        _openapi_v2_cache = get_openapi(
            title="OBDX / RPM & Modern Digital Banking - Collection v2",
            version="2.0.0",
            description="""
### Collection v2: Oracle OBDX / RPM & Next-Gen Digital Banking
- **OBDX / RPM Services:** Business Products Catalog, Origination Process Driver (Initiate, Submit, GetData, GetDocumentList), Application Search & Inquiry.
- **Next-Gen Digital Banking:** Account 360 Information, Full Account Statements, Loans Portfolio & Amortization Schedules, Loan Applications, Term Deposits (FD/RD), and Fund Transfers.
""",
            routes=router_v2.routes
        )
    return _openapi_v2_cache


@app.get("/openapi-v3.json", include_in_schema=False)
async def get_openapi_v3():
    global _openapi_v3_cache
    if _openapi_v3_cache is None:
        _openapi_v3_cache = get_openapi(
            title="Unified Oracle FLEXCUBE & Digital Banking - Collection v3",
            version="3.0.0",
            description="""
### Collection v3: Combined & Unified Oracle FLEXCUBE CBS & Digital Banking API
- **Symmetrical POST Core API Contracts:** Unified endpoint structure based on canonical CBS integration patterns.
- **Enriched 360 Account Data:** Includes IFSC, Branch Details, Lien Amount, Uncleared Balances, Nominees, Joint Holders, and Linked Cards without losing any legacy fields.
- **Complete Suite:** Customer Inquiries, Account Statements with Transaction Ledgers, Cards Management, Cheque Clearing & Stop Payments, Tax Certificates, Lockers, Loans with Amortization Schedules, Term Deposits (Open & Pre-closure), Funds Transfers, and RPM Business Products & Origination Workflow.
- **Dual Envelopes:** XML (`application/xml`) with `<CBSRequest>`/`<CBSResponse>` and JSON (`application/json`).
""",
            routes=router_v3.routes
        )
    return _openapi_v3_cache


@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def custom_swagger_ui_html():
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <title>Oracle CBS & OBDX Mock API - Swagger UI</title>
    <style>
        html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
        *, *:before, *:after { box-sizing: inherit; }
        body { margin: 0; background: #fafafa; }
        .swagger-ui .topbar {
            background-color: #1a202c !important;
            padding: 10px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .swagger-ui .topbar .download-url-wrapper {
            display: flex;
            align-items: center;
        }
        .swagger-ui .topbar select {
            background: #ffffff !important;
            color: #2d3748 !important;
            padding: 8px 14px !important;
            border-radius: 6px !important;
            font-size: 14px !important;
            border: 1px solid #cbd5e0 !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            outline: none;
        }
        .swagger-ui .topbar select:focus {
            border-color: #3182ce !important;
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
                    name: "v3 - Unified FLEXCUBE & Digital Banking (Recommended)",
                    url: "/openapi-v3.json"
                },
                {
                    name: "v1 - Core Banking System (CBS)",
                    url: "/openapi-v1.json"
                },
                {
                    name: "v2 - OBDX / RPM & Digital Banking",
                    url: "/openapi-v2.json"
                },
                {
                    name: "All APIs (Combined)",
                    url: "/openapi.json"
                }
            ],
            "urls.primaryName": "v3 - Unified FLEXCUBE & Digital Banking (Recommended)",
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


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "UP", "service": "cbs-obdx-mock-server", "versions": ["v1", "v2", "v3"]}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting CBS, OBDX & Unified Mock Server on 0.0.0.0:8000...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
