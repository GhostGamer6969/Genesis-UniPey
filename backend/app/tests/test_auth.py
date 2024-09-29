import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.database import Base, engine, SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_request_otp(setup_database):
    response = client.post("/auth/request-otp", json={"phone_number": "1234567890"})
    assert response.status_code == 200
    assert response.json()["detail"] == "OTP Sent Successfully"

def test_verify_otp(setup_database):
    response = client.post("/auth/request-otp", json={"phone_number": "1234567890"})
    transaction_id = response.json()["transaction_id"]

    # Simulate OTP received
    response = client.post("/auth/verify-otp", json={"transaction_id": transaction_id, "otp": "123456"})
    assert response.status_code == 200
    assert response.json()["detail"] == "OTP Verified Successfully"
