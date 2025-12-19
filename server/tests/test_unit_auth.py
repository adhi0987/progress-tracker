import pytest
from server.auth.auth import get_password_hash, verify_password, create_access_token
from jose import jwt
import os

def test_password_hashing():
    password = "secret_password"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    # Decode to verify contents
    secret = os.getenv("SECRET_KEY", "supersecretkey")
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    
    assert payload["sub"] == "testuser"
    assert "exp" in payload