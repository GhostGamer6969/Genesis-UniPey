import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.db_schemas.sessions import SessionDb
from app.utils.models import UserSession

def create_session(db: Session, user_id: uuid.UUID, ip_address: str) -> UserSession:
    session_id = uuid.uuid4()
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(days=1)  # Example session duration

    db_session = SessionDb(
        id=session_id,
        user_id=user_id,
        created_at=created_at,
        expires_at=expires_at,
        ip_address=ip_address,
    )
    db.add(db_session)
    db.commit()

    return UserSession(
        id=session_id,
        created_at=created_at,
        expires_at=expires_at,
    )
