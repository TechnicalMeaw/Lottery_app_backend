from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/transaction",
    tags=["Transaction"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def transact(transactionData : schemas.TransactionRequest, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    prevTransactionOnSameId = db.query(models.Transactions).filter(models.Transactions.user_id == current_user.id, models.Transactions.transction_id == transactionData.transction_id).first()

    if prevTransactionOnSameId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Transaction id already exists")
    
    new_transaction = models.Transactions(user_id = current_user.id, **transactionData.dict())
    db.add(new_transaction)

    return {"details": "Transaction added, need to be verified"}


@router.post("/verify")
def verify_transaction(verificationData: schemas.VerifyTransactionRequest, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    transaction = db.query(models.Transactions).filter(models.Transactions.user_id == verificationData.user_id).filter(models.Transactions.transction_id == verificationData.transaction_id).filter(models.Transactions.id == verificationData.in_app_transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Transaction does not exists")
    
    # Get prev balance
    coin_balance_query = db.query(models.Coins).filter(models.Coins.user_id == verificationData.user_id)
    user_coin_balance = coin_balance_query.first()
    
    if verificationData.is_verified:
        transaction.is_verified = True
        
        # Update the coin balance
        if not user_coin_balance:
            new_coin_balance = schemas.CoinResponse(num_of_coins=transaction.amount, coin_type=1)
            new_coins_row = models.Coins(**new_coin_balance.dict())
            new_coins_row.user_id = current_user.id
            db.add(new_coins_row)
            db.commit()
            return new_coin_balance
        

        user_coin_balance.num_of_coins += transaction.amount

        db.commit()
        return user_coin_balance
    
    else:
        transaction.is_verified = False
        transaction.is_rejected_by_admin = True
        db.commit()

        # Get coin balance
        new_coin_balance = schemas.CoinResponse(num_of_coins=transaction.amount, coin_type=1)
        new_coins_row = models.Coins(**new_coin_balance.dict())
        new_coins_row.user_id = current_user.id

        return new_coin_balance

    
