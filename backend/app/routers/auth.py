import uuid
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from eth_account import Account
from app.utils.database import get_db
from app.db_schemas.user import UserDb
from app.db_schemas.otp_transaction import OTPTransactionsDb
from app.utils.models import (
    PhoneNumberRequest,
    OTPVerifyRequest,
    UserSignUpRequest,
    UserSignUpResponse,
    CompleteSignUpResponse,
    UserSession,
    UserLoginResponse,
    CompleteLoginResponse,
)
from app.utils import sessions as session_utils
from app.config import settings
from app.logging import logger
from app.utils.twilio_client import send_otp_via_twilio
from app.utils.hashing import hash_password, check_password
from app.utils.stellar_utils import create_wallet, get_balance, convert_to_usd

router = APIRouter(tags=["Auth"], prefix="/auth")

def create_erc20_address():
    # Generate a new Ethereum address
    acct = Account.create()
    return acct.address

@router.post("/request-otp", response_model=UserSignUpResponse)
def request_otp(request: Request, phone_request: PhoneNumberRequest, db: Session = Depends(get_db)):
    """Request for OTP. Decides whether to login or signup based on phone number existence."""
    phone_number = phone_request.phone_number

    # Check if the user already exists
    db_user = db.query(UserDb).filter(UserDb.phone_number == phone_number).first()

    # Delete any ongoing OTP transaction for the same phone number
    db_transaction = (
        db.query(OTPTransactionsDb)
        .filter(OTPTransactionsDb.phone_number == phone_number)
        .filter(OTPTransactionsDb.is_otp_verified == False)
        .first()
    )
    if db_transaction:
        db.delete(db_transaction)
        db.commit()

    # Generate OTP
    generated_otp = "".join(secrets.choice("0123456789") for _ in range(6))

    # Send OTP via Twilio
    send_otp_via_twilio(phone_number, generated_otp)

    # Save the OTP transaction
    db_otp_transaction = OTPTransactionsDb(
        id=uuid.uuid4(),  # Generate UUID for transaction ID
        phone_number=phone_number,
        code=generated_otp,
        created_at=datetime.now(timezone.utc),
        otp_expires_at=datetime.now(timezone.utc) + timedelta(seconds=settings.OTP_EXPIRY_IN_SECONDS),
        transaction_expires_at=datetime.now(timezone.utc) + timedelta(seconds=settings.OTP_TRANSACTION_EXPIRY_IN_SECONDS),
        ip_address=request.client.host
    )
    db.add(db_otp_transaction)
    db.commit()
    db.refresh(db_otp_transaction)

    return JSONResponse(
        content=jsonable_encoder(
            UserSignUpResponse(
                detail="OTP Sent Successfully",
                transaction_id=db_otp_transaction.id,
                otp_expires_at=db_otp_transaction.otp_expires_at,
            )
        ),
        status_code=status.HTTP_200_OK,
    )

@router.post("/verify-otp", response_model=UserSignUpResponse)
def verify_otp(request: Request, otp_request: OTPVerifyRequest, db: Session = Depends(get_db)):
    """Verify the OTP and decide whether to login or proceed to signup."""
    db_transaction = db.query(OTPTransactionsDb).filter(OTPTransactionsDb.id == otp_request.transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Transaction ID")

    if db_transaction.otp_expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired")

    if db_transaction.code != otp_request.otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

    db_transaction.is_otp_verified = True
    db.commit()

    db_user = db.query(UserDb).filter(UserDb.phone_number == db_transaction.phone_number).first()
    if db_user:
        # User exists, create a session
        session = session_utils.create_session(db, db_user.id, request.client.host)
        return JSONResponse(
            content=jsonable_encoder(
                CompleteLoginResponse(detail="Login Successful", session=session)
            ),
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content=jsonable_encoder(
            UserSignUpResponse(
                detail="OTP Verified Successfully. User does not exist, proceed to signup.",
                transaction_id=db_transaction.id,
                otp_expires_at=db_transaction.otp_expires_at,
            )
        ),
        status_code=status.HTTP_201_CREATED,  # Use 201 Created to indicate signup is needed
    )

@router.post("/complete-signup", response_model=CompleteSignUpResponse)
def complete_signup(request: Request, signup_request: UserSignUpRequest, db: Session = Depends(get_db)):
    """Complete the signup process."""
    db_transaction = db.query(OTPTransactionsDb).filter(OTPTransactionsDb.id == signup_request.transaction_id).first()
    if not db_transaction or not db_transaction.is_otp_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or unverified transaction")

    # Create a new user
    password_hash, salt = hash_password(signup_request.password)
    stellar_wallet = create_wallet()
    erc20_address = create_erc20_address()
    db_user = UserDb(
        id=uuid.uuid4(),  # Generate UUID for user ID
        phone_number=db_transaction.phone_number,
        password_hash=password_hash,
        password_salt=salt,
        first_name=signup_request.first_name,
        last_name=signup_request.last_name,
        dob=signup_request.dob,
        gender=signup_request.gender,
        created_at=datetime.now(timezone.utc),
        stellar_public_key=stellar_wallet["public_key"],
        stellar_secret_key=stellar_wallet["secret_key"],
        erc20_address=erc20_address,  # Store ERC20 address
    )
    db.add(db_user)
    db.commit()

    # Remove the OTP transaction
    db.delete(db_transaction)
    db.commit()

    # Create a new session
    session = session_utils.create_session(db, db_user.id, request.client.host)

    return JSONResponse(
        content=jsonable_encoder(
            CompleteSignUpResponse(detail="Signup Successful", session=session)
        ),
        status_code=status.HTTP_200_OK,
    )

@router.get("/wallet/{user_id}")
def get_wallet(user_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get wallet balance and USD equivalent for a user."""
    user = db.query(UserDb).filter(UserDb.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    balance = get_balance(user.stellar_public_key)
    if balance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

    usd_equivalent = convert_to_usd(balance)
    return {"balance": balance, "usd_equivalent": usd_equivalent}
