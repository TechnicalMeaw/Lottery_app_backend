from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

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