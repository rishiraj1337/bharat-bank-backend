from fastapi import APIRouter

# Import V1 routers that are part of the V2 superset
from digital_backend.routers.flutter import system as flutter_system
from digital_backend.routers.flutter import dashboard as flutter_dashboard
from digital_backend.routers.flutter import accounts as flutter_accounts
from digital_backend.routers.flutter import transfers as flutter_transfers
from digital_backend.routers.flutter import beneficiaries as flutter_beneficiaries
from digital_backend.routers.flutter import cards as flutter_cards
from digital_backend.routers.flutter import loans as flutter_loans
from digital_backend.routers.flutter import cheques as flutter_cheques
from digital_backend.routers.flutter import services as flutter_services

# Import V2-enhanced routers
from digital_backend.routers.flutter_v2 import auth as auth_v2
from digital_backend.routers.flutter_v2 import profile as profile_v2
from digital_backend.routers.flutter_v2 import notifications as notifications_v2
from digital_backend.routers.flutter_v2 import deposits as deposits_v2
from digital_backend.routers.flutter_v2 import bill_payments as bill_payments_v2

# Master Router for Flutter Mobile App v2 (Prefix: /api/v2/app)
flutter_v2_master_router = APIRouter(prefix="/api/v2/app")

# Core system, theme & dashboard
flutter_v2_master_router.include_router(flutter_system.router)
flutter_v2_master_router.include_router(flutter_dashboard.router)

# Auth & Security (with Logout)
flutter_v2_master_router.include_router(auth_v2.router)

# Customer Profile (New in v2)
flutter_v2_master_router.include_router(profile_v2.router)

# In-App Notifications (New in v2)
flutter_v2_master_router.include_router(notifications_v2.router)

# Accounts & Transfers
flutter_v2_master_router.include_router(flutter_accounts.router)
flutter_v2_master_router.include_router(flutter_transfers.router)
flutter_v2_master_router.include_router(flutter_beneficiaries.router)

# Cards & Loans
flutter_v2_master_router.include_router(flutter_cards.router)
flutter_v2_master_router.include_router(flutter_loans.router)

# Term Deposits (with Open-RD)
flutter_v2_master_router.include_router(deposits_v2.router)

# BBPS & Bill Payments (with Schedule, Recurring, Registered Billers, Status)
flutter_v2_master_router.include_router(bill_payments_v2.router)

# Cheques & Ancillary Banking Services
flutter_v2_master_router.include_router(flutter_cheques.router)
flutter_v2_master_router.include_router(flutter_services.router)
