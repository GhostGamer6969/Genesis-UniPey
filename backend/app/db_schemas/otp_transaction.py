import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.utils.database import Base

class OTPTransactionsDb(Base):
    __tablename__ = "otp_transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    phone_number = Column(String, index=True, nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    otp_expires_at = Column(DateTime, nullable=False)
    transaction_expires_at = Column(DateTime, nullable=False)
    is_otp_verified = Column(Boolean, default=False, nullable=False)
    ip_address = Column(String, nullable=False)
