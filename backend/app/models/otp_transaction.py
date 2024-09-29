from pydantic import BaseModel
from datetime import datetime

class OTPTransaction(BaseModel):
    phone_number: str
    code: str
    created_at: datetime
    otp_expires_at: datetime
    transaction_expires_at: datetime
    is_otp_verified: bool
    ip_address: str
