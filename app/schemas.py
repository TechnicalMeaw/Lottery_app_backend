from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Create User Request Model
class UserCreate(BaseModel):
    name: str
    phone_no: str
    password: str
    refferal : Optional[str]

# User login response model
class UserOut(BaseModel):
    id: int
    name: str
    phone_no: str
    created_at : datetime

    class Config:
        orm_mode = True


class UserOutWithRefferal(UserOut):
    refferal : str

    class Config:
        orm_mode = True


class UserOutWithCoin(BaseModel):
    User : UserOut
    coins : Optional[int]

    class Config:
        orm_mode = True

# User login request model
class UserLogin(BaseModel):
    phone_no : str
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
            "example": {"detail": "HTTPException string / Success string"},
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
    user_id : int
    transaction_id : str
    in_app_transaction_id : int
    is_verified : bool


#  Individualtransaction response
class IndividualTransactionResponse(BaseModel):
    id : int
    amount : int
    transction_id : str
    isAdded : bool
    transaction_medium : str
    is_verified : bool
    is_rejected_by_admin : bool
    screenshot_url : str
    created_at : datetime

    class Config:
        orm_mode = True


# All transaction response
class Transaction(IndividualTransactionResponse):
    user_id : int
    user : UserOut

    class Config:
        orm_mode = True


# Withdraw
class WithdrawRequest(BaseModel):
    phone_no : str
    transaction_medium : str
    amount : int

class VerifyWithdrawRequest(BaseModel):
    withdraw_id : int
    is_verified : bool


class WithdrawIndividualResponse(BaseModel):
    id : int
    amount : int
    phone_no : str
    transaction_medium : str
    is_verified : bool
    is_rejected_by_admin : bool
    created_at : datetime

    class Config:
        orm_mode = True


class WithdrawResponse(WithdrawIndividualResponse):
    user_id : int
    user : UserOut

    class Config:
        orm_mode = True


# Send Otp request
class EmailSchema(BaseModel):
   email: List[EmailStr]

# verify Otp
class OtpVerifyRequest(BaseModel):
    phone: str

class ChangePasswordRequest(BaseModel):
    phone_no : str
    newPassword: str


class LotteryOutResponse(BaseModel):
    lottery_token: int
    is_winner : bool
    user : UserOut

    class Config:
        orm_mode = True

# Lottery Buy Response
class BuyLotteryRequest(BaseModel):
    amount: int
    timeZoneOffsetFromUtc : Optional[int]


class TimeLeftResponse(BaseModel):
    time_left_in_millis : str

    class Config:
        orm_mode = True


class LotteryWinner(BaseModel):
    lottery_token_no : int
    position : int

    user : UserOut

    class Config:
        orm_mode = True


class SetLotteryWinnerRequest(BaseModel):
    token: int
    rank: int

class RemoveLotteryWinnerRequest(BaseModel):
    token: int


# Lottery Prize
class LotteryPrize(BaseModel):
    rank_no : int
    prize_money : int

    class Config:
        orm_mode = True


class LotteryPrizeDeleteRequest(BaseModel):
    rank_no: int


# Refferal response
class RefferalResponse(BaseModel):
    User : UserOut
    reffered_user_id : int
    amount : int
    is_success : bool
    created_at : datetime

    class Config:
        orm_mode = True


class HorseMatchTiming(BaseModel):

    is_horse_bidding_slot_open : bool
    remaining_time_in_millis : int


class HorseRaceWinnerResponseModel(BaseModel):
    bid_amount : Optional[int]

    class Config:
        orm_mode = True

class HorseRaceWinnerDetailsResponseModel(BaseModel):
    winnig_horse_id : int
    is_user_winner : bool
    total_bid_money : int
    bid_on_winning_horse : int = 0
    win_money : int = 0

    class Config:
        orm_mode = True


class HorseRaceBidRequestModel(BaseModel):
    bid_horse_id : int
    bid_amount : int


class HorseRaceMyBidsResponseModel(BaseModel):
    horse_id : int
    bid_amount : int

    class Config:
        orm_mode = True


# Request Model
class AddTransactionMediumRequestModel(BaseModel):
    medium_title : str

#  Response Model
class TransactionMedium(BaseModel):
    id : int
    medium_title : str
    created_at : datetime

    class Config:
        orm_mode = True

# Delete Request Model
class DeleteTransactionMediumRequestModel(BaseModel):
    id : int


#  Response Model
class LuckyDrawCoinValues(BaseModel):
    id : int
    coin_value : int
    created_at : datetime

    class Config:
        orm_mode = True

# Modify Request Model
class ModifyLuckyDrawCoinRequestModel(BaseModel):
    id : int
    coin_value : int
    


class LotteryNoticeRequestResponseModel(BaseModel):
    notice_text : str

    class Config:
        orm_mode = True


class JhandiMundaTiming(BaseModel):

    is_jhandi_munda_slot_open : bool
    remaining_time_in_millis : int


class JhandiMundaBidRequestModel(BaseModel):
    bid_card_id : int
    bid_amount : int


class JhandiMundaWinnerDetailsResponseModel(BaseModel):
    winnig_card_id : int
    is_user_winner : bool
    total_bid_money : int
    bid_on_winning_card : int = 0
    win_money : int = 0

    class Config:
        orm_mode = True


class JhandiMundaMyBidsResponseModel(BaseModel):
    card_id : int
    bid_amount : int

    class Config:
        orm_mode = True