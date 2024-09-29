from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PhoneNumberRequest(BaseModel):
    phone_number: str

class OTPVerifyRequest(BaseModel):
    transaction_id: UUID
    otp: str

class UserSignUpRequest(BaseModel):
    transaction_id: UUID
    first_name: str
    last_name: str
    phone_number: str
    password: str
    dob: datetime
    gender: str

class UserSignUpResponse(BaseModel):
    detail: str
    transaction_id: UUID
    otp_expires_at: datetime

class CompleteSignUpResponse(BaseModel):
    detail: str
    session: 'UserSession'

class UserSession(BaseModel):
    id: UUID
    created_at: datetime
    expires_at: datetime

class UserLoginResponse(BaseModel):
    detail: str
    transaction_id: UUID
    otp_expires_at: datetime

class CompleteLoginResponse(BaseModel):
    detail: str
    session: UserSession

class WalletResponse(BaseModel):
    usdc_balance: float
    usd_equivalent: float
