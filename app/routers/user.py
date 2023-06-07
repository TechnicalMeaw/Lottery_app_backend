from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.sql.expression import cast
from sqlalchemy import String

router = APIRouter(
    prefix= "/users",
    tags=["Users"]
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut, 
             responses={status.HTTP_201_CREATED: {"model" : schemas.UserOut}, 
                        status.HTTP_403_FORBIDDEN : {"model": schemas.HTTPError,"description": "If user already exists"}})
def create_user(user : schemas.UserCreate, db: Session = Depends(get_db)):

    # Check if user already exists
    existing_phone_no = db.query(models.User).filter(models.User.phone_no == user.phone_no).first()

    if existing_phone_no:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    
    country_code, number = utils.split_phone_number(user.phone_no)

    if not country_code or not number:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid phone number")

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user.phone_no = number

    new_user = models.User(country_code = country_code, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/get_all_user_info", response_model=List[schemas.UserOutWithCoin])
def get_all_users(page_no : int = 1, search_phone_number: Optional[str] = "", db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    query = db.query(models.User, models.Coins.num_of_coins.label("coins")).join(models.Coins, models.User.id == models.Coins.user_id, isouter=True).filter(cast(models.User.phone_no, String).contains(search_phone_number)).limit(10).offset((page_no-1)*10)


    all_users = query.all()

    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return all_users


@router.get("/", response_model= schemas.UserOut)
def get_current_user(db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User does not exist")
    
    return user


@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User with id: {id} does not exist")
    
    return user

