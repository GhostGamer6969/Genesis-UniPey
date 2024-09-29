from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    OTP_EXPIRY_IN_SECONDS: int = 300
    OTP_TRANSACTION_EXPIRY_IN_SECONDS: int = 1800
    DATABASE_URL: str  # Change to str instead of PostgresDsn
    STELLAR_BLAZE_PUBLIC_KEY: str 
    STELLAR_BLAZE_SECRET_KEY: str 

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields

settings = Settings()
#print(settings.dict())
print(settings.model_dump())