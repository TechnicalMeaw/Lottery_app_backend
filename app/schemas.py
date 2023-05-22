from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Create User Request Model
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# User login response model
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

# User login request model
class UserLogin(BaseModel):
    email : EmailStr
    password : str

# Token response model
class Token(BaseModel):
    access_token : str
    token_type : str

# For token verification
class TokenData(BaseModel):
    id : Optional[str] = None


# Model for error messege
class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException string"},
        }

# Model for coin updation request
class CoinUpdateRequest(BaseModel):
    coins : int
    updation_type : str


class CoinResponse(BaseModel):
    num_of_coins: int
    coin_type: int

    class Config:
        orm_mode = True

# For transaction request
class TransactionRequest(BaseModel):
    amount : int
    transction_id : str
    isAdded : bool
    transaction_medium : str
    screenshot_url : str

# For transaction verification request --- Admin Panel
class VerifyTransactionRequest(BaseModel):
    user_id : bool
    transaction_id : str
    in_app_transaction_id : int
    is_verified : bool

# Send Otp request
class EmailSchema(BaseModel):
   email: List[EmailStr]

# verify Otp
class OtpVerifyRequest(BaseModel):
    email: EmailStr
    otp: int

class ChangePasswordRequest(BaseModel):
    newPassword: str


class LotteryOutResponse(BaseModel):
    lottery_token: int
    is_winner : bool

    class Config:
        orm_mode = True

# Lottery Buy Response
class LotteryBuyResponse(BaseModel):
    lottery_entries : List[LotteryOutResponse]