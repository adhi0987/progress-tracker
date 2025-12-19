import pytest
from unittest.mock import patch, AsyncMock
from server.services.UserServices import UserService
from server.schemas.signupRequestModel import SignupRequestModel
from fastapi import HTTPException

@pytest.mark.anyio
async def test_create_user_service_success(db_session):
    # Prepare data
    user_data = SignupRequestModel(
        username="service_user",
        email="service@test.com",
        name="Service User",
        password="password123"
    )

    # Mock Permit.io calls
    with patch("server.services.UserServices.permit") as mock_permit:
        mock_permit.api.users.sync = AsyncMock(return_value=True)
        mock_permit.api.users.assign_role = AsyncMock(return_value=True)
        
        new_user = await UserService.create_user(db_session, user_data)
        
        assert new_user.username == "service_user"
        assert new_user.email == "service@test.com"

@pytest.mark.anyio
async def test_create_user_rollback_on_permit_failure(db_session):
    user_data = SignupRequestModel(
        username="fail_user", email="f@e.com", name="F", password="p"
    )

    # Mock Permit to throw an error
    with patch("server.services.UserServices.permit") as mock_permit:
        mock_permit.api.users.sync.side_effect = Exception("Permit Error")
        
        with pytest.raises(HTTPException) as exc:
            await UserService.create_user(db_session, user_data)
        
        assert exc.value.status_code == 500
        # Verify user was deleted from DB (rolled back)
        user_in_db = UserService.get_user_by_username(db_session, "fail_user")
        assert user_in_db is None