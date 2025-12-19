import pytest
from httpx import AsyncClient, ASGITransport
from server.app import app
from unittest.mock import patch, AsyncMock

@pytest.mark.anyio
async def test_full_login_flow(anyio_backend):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Signup
        signup_data = {
            "username": "login_user", 
            "password": "securepassword", 
            "email": "login@test.com", 
            "name": "Login User"
        }
        with patch("server.services.UserServices.permit") as mock_permit:
            mock_permit.api.users.sync = AsyncMock()
            mock_permit.api.users.assign_role = AsyncMock()
            await ac.post("/api/signup", json=signup_data)

        # 2. Login
        login_data = {"username": "login_user", "password": "securepassword"}
        # Assuming your login endpoint uses OAuth2 form data or JSON
        response = await ac.post("/api/login", json=login_data) 
        
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.anyio
async def test_unauthorized_access(anyio_backend):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Attempt to get PDFs without a token
        response = await ac.get("/api/pdfs")
        assert response.status_code == 401