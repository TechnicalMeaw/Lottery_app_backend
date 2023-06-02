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

    if len(user_credentials.username)  < 11:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    country_code, number = utils.split_phone_number(user_credentials.username)

    user = db.query(models.User).filter(models.User.phone_no == number).filter(models.User.country_code == country_code).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="First verify your phone number")
    
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}



# @router.post("/send_otp")
# async def send_otp(email: schemas.EmailSchema, db: Session = Depends(get_db)):
#     otp = generateOtp()

#     prev_otp_entry = db.query(models.OTPs).filter(models.OTPs.user_email == email.email[0]).first()

#     if not prev_otp_entry:
#         print(email.email[0])
#         new_otp = models.OTPs(user_email = email.email[0], otp = otp)
#         db.add(new_otp)
#         db.commit()

#     else:
#         prev_otp_entry.otp = otp
#         db.commit()

#     await sendOTP(email.email, otp)
#     return {"details": "OTP sent"}


@router.post("/verify_otp")
def verify_otp(otpData: schemas.OtpVerifyRequest, db: Session = Depends(get_db)):

    # prev_otp_entry = db.query(models.OTPs).filter(models.OTPs.user_email == otpData.email).first()

    # # If otp not sent
    # if not prev_otp_entry:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OTP was never sent to this email")
    
    # # If otp expired
    # if datetime.strftime(prev_otp_entry.created_at + timedelta(minutes=5), "%d/%m/%y %H:%M:%S") < datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S"):
    #     raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="OTP expired.")
    
    user_entry = db.query(models.User).filter(models.User.phone_no == otpData.phone).first()

    # if not user_entry:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    # if int(prev_otp_entry.otp) != otpData.otp:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Otp does not match")

    user_entry.is_verified = True

    db.commit()

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user_entry.id})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/change_password")
def change_password(passwordData: schemas.ChangePasswordRequest, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == current_user.id).first()

    db_user.password = utils.hash(passwordData.newPassword)
    db.commit()

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}




