from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class UserDb(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    password_salt = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    dob = Column(DateTime, nullable=True)
    gender = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    stellar_public_key = Column(String, nullable=True)
    stellar_secret_key = Column(String, nullable=True)
    erc20_address = Column(String, nullable=True)
