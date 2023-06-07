from fastapi import status, HTTPException, Depends, APIRouter
from datetime import datetime, timedelta

from app.otp_util import generateOtp, sendOTP
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.phone_no == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="First verify your phone number")
    
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/change_password")
def change_password(passwordData: schemas.ChangePasswordRequest, db: Session = Depends(get_db)):
    country_code, number = utils.split_phone_number(passwordData.phone_no)

    db_user = db.query(models.User).filter(models.User.phone_no == number).filter(models.User.country_code == country_code).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists")

    db_user.password = utils.hash(passwordData.newPassword)
    db.commit()

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}




