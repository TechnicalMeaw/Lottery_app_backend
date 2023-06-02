from passlib.context import CryptContext
from datetime import datetime
from sqlalchemy.orm import Session
from . import models
from datetime import time
import re


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_lottery_time_left_in_millis():
    now = datetime.now()
    nine_pm = datetime(now.year, now.month, now.day, 21, 0, 0)  # Set the time to 9 PM

    # Calculate the time difference in milliseconds
    time_difference = (nine_pm - now).total_seconds() * 1000
    return int(time_difference)



def is_lottery_active():

    now = datetime.now()
    nine_pm = datetime(now.year, now.month, now.day, 10, 0, 0)  # Set the time to 9 PM

    # Calculate the time difference in milliseconds
    time_difference = (nine_pm - now).total_seconds() * 1000
    return get_lottery_time_left_in_millis() > 0 and int(time_difference) < 0
    



def delete_prev_lottery_data(db: Session):
    now = datetime.now()
    db.query(models.Lottery).filter(models.Lottery.created_at < datetime(now.year, now.month, now.day, 10, 0, 0)).delete()

    db.commit()


def split_phone_number(phone_number):
    pattern = r'^(\+\d{1,3})(\d{10}+)$'
    match = re.match(pattern, phone_number)
    if match:
        country_code = match.group(1)
        number = match.group(2)
        return country_code, number
    else:
        return None, None