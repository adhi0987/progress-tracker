import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from server.app import app

@pytest.mark.anyio
async def test_signup_integration(anyio_backend):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        signup_data = {
            "name": "Test User",
            "email": "test_unique@example.com",
            "username": "testuser_unique",
            "password": "testpassword123"
        }
        with patch("server.services.UserServices.permit.api.sync_user") as mock_sync:
            mock_sync.return_value = True 
            response = await ac.post("/api/signup", json=signup_data)
    
    assert response.status_code == 200