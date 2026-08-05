import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///erp_demo.db")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

# Config sandbox documentada (no activa en MVP)
SANDBOX_CONFIG = {
    "gocardless": {
        "name": "GoCardless Bank Account Data",
        "sandbox_url": "https://developer.gocardless.com/bank-account-data/quickstart",
        "notes": "Regístrate, crea app en sandbox, obtén access_token y secret_id"
    },
    "plaid": {
        "name": "Plaid",
        "sandbox_url": "https://plaid.com/docs/quickstart/",
        "notes": "Cuenta sandbox gratuita. Usa environment='sandbox'"
    },
    "google_ads": {
        "name": "Google Ads API",
        "sandbox_url": "https://developers.google.com/google-ads/api/docs/start",
        "notes": "Necesitas cuenta de Google Ads de prueba (CID 0) y developer token"
    },
    "meta_ads": {
        "name": "Meta Marketing API",
        "sandbox_url": "https://developers.facebook.com/docs/marketing-api/overview",
        "notes": "Usa Graph API Explorer con token de prueba"
    }
}
