import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.app import app
from server.database.database import Base, get_db

# 1. Setup a separate test database (SQLite in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Dependency override: tell FastAPI to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def anyio_backend():
    return 'asyncio'
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from server.app import app
from server.database.database import Base, get_db

# 1. Setup a separate test database (SQLite in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Dependency override: tell FastAPI to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Explicitly set the backend to 'asyncio' to avoid Trio errors
@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.mark.anyio
async def test_signup_integration(anyio_backend):
    # Create tables in the in-memory database
    Base.metadata.create_all(bind=engine)
    
    # Mock Permit.io sync to avoid network calls/errors
    with patch("server.services.UserServices.permit.api.sync_user") as mock_sync:
        mock_sync.return_value = True 
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            signup_data = {
                "name": "Test User",
                "email": "test@example.com",
                "username": "testuser_unique",
                "password": "testpassword123"
            }
            # The URL matches the prefix defined in app.py
            response = await ac.post("/api/signup", json=signup_data)
    
    # Assertions
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
    # Cleanup for next test
    Base.metadata.drop_all(bind=engine)

@pytest.mark.anyio
async def test_signup_duplicate_username(anyio_backend):
    Base.metadata.create_all(bind=engine)
    
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "username": "duplicate_user",
        "password": "password123"
    }

    with patch("server.services.UserServices.permit.api.sync_user") as mock_sync:
        mock_sync.return_value = True
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            # First attempt
            await ac.post("/api/signup", json=signup_data)
            # Second attempt with same username
            response = await ac.post("/api/signup", json=signup_data)
    
    # Should raise 400 Bad Request as defined in UserServices
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"
    
    Base.metadata.drop_all(bind=engine)
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_signup_integration(anyio_backend):
    # Create tables in the in-memory database
    Base.metadata.create_all(bind=engine)
    
    # Use ASGITransport for FastAPI testing
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        signup_data = {
            "name": "Test User",
            "email": "test@example.com",
            "username": "testuser_unique",
            "password": "testpassword123"
        }
        response = await ac.post("/api/signup", json=signup_data)
    
    # Assertions
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)