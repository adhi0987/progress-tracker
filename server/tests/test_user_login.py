import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from server.app import app

@pytest.mark.anyio
async def test_login_integration(anyio_backend):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Create user
        signup_data = {"username": "user1", "password": "pass", "email": "u1@e.com", "name": "U1"}
        with patch("server.services.UserServices.permit.api.sync_user") as mock:
            mock.return_value = True
            await ac.post("/api/signup", json=signup_data)

        # Login
        login_data = {"username": "user1", "password": "pass"}
        # Note: If your login uses Form data, use 'data=login_data'. If JSON, use 'json=login_data'
        response = await ac.post("/api/login", json=login_data)
        
        # Adjust this assertion based on your expected logic (e.g., 200)
        assert response.status_code == 200