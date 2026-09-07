import os
from pydantic import BaseModel

class BackendSettings(BaseModel):
    app_name: str = "Bharat Bank Omnichannel Digital Banking Backend"
    version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    port: int = int(os.getenv("PORT", "8080"))
    host: str = os.getenv("HOST", "0.0.0.0")
    cbs_base_url: str = os.getenv("CBS_BASE_URL", "http://localhost:8000")
    log_to_file: bool = True
    log_file_path: str = "digital_backend/logs/digital_backend.log"

settings = BackendSettings()
