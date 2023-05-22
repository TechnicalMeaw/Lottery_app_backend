from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/lottery",
    tags=["Lottery"]
)

@router.get("/buy/{amount}", response_model=schemas.LotteryBuyResponse)
def buy_lottery(amount: int, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    coin_balance = db.query(models.Coins).filter(current_user.id == models.Coins.user_id).first()

    if not coin_balance:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Coin Balance is not enough")
    
    if int(coin_balance.num_of_coins) < amount:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Coin Balance is not enough")

    lottery_entry = models.Lottery(user_id = current_user.id)
    
    db.add(lottery_entry)
    coin_balance.num_of_coins -= amount

    db.commit()

    user_entries = db.query(models.Lottery).filter(models.Lottery.user_id == current_user.id).all()

    return user_entries