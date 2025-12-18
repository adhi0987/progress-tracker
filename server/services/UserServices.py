from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import server.models.models as models
# import server.schemas.schemas as schemas
from  server.schemas.signupRequestModel import SignupRequestModel;
from server.schemas.loginRequestModel import  LoginRequestModel
import  server.auth.auth  as auth 
from server.auth.permitConfig import permit

class UserService:
    @staticmethod
    async def create_user(db:Session, user:SignupRequestModel):
        #check if user already exists
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
        hashed_password = auth.get_password_hash(user.password)
        new_user = models.User(
            username=user.username,
            email=user.email,
            name=user.name,
            password_hash=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        #sync the user with permit.io
        
        try:
            await permit.api.users.sync(
                {
                    "key":user.username,
                    "email":user.email,
                    "first_name":user.name,
                    "last_name":""
                }
            )
        except Exception as e:
            print(e)
            db.delete(new_user)
            db.commit()
            print("Error syncing user with permission service, rolling back user creation")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error syncing user with permission service")
        try:
            #assign default role to user
            await permit.api.users.assign_role(
                {
                    "user":user.username,
                    "role":"user",
                    "tenant":"default"
                }
            )
        except Exception as e:
            print(e)
            db.delete(new_user)
            db.commit()
            print("Error assigning role to user, rolling back user creation")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error assigning role to user in permission service")
        return new_user
    @staticmethod
    def authenticate_user(db:Session,user:LoginRequestModel):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if not db_user or not auth.verify_password(user.password, db_user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        return db_user
    @staticmethod
    def get_user_by_username(db:Session,username:str):
        return db.query(models.User).filter(models.User.username == username).first()