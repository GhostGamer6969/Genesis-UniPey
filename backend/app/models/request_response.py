from pydantic import BaseModel
from datetime import datetime, date

class PhoneNumberRequest(BaseModel):
    phone_number: str

class OTPVerifyRequest(BaseModel):
    transaction_id: int
    otp: str

class UserSignUpRequest(BaseModel):
    transaction_id: int
    first_name: str
    last_name: str
    password: str
    dob: date
    gender: str

class UserSignUpResponse(BaseModel):
    detail: str
    transaction_id: int
    otp_expires_at: datetime

class CompleteSignUpResponse(BaseModel):
    detail: str
    session: dict

class UserSession(BaseModel):
    session_id: str
    user_id: int
    created_at: datetime
    expires_at: datetime

class UserLoginResponse(BaseModel):
    detail: str
    transaction_id: int
    otp_expires_at: datetime

class CompleteLoginResponse(BaseModel):
    session: dict
