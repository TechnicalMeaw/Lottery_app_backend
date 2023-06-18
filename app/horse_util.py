from passlib.context import CryptContext
from datetime import datetime
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import time
import re
from sqlalchemy import func


def get_lottery_time_left_in_millis():
    now = datetime.now()

    if now.minute == 0 or (now.minute == 1 and now.second < 30):
        current_match_end_time = datetime(now.year, now.month, now.day, now.hour, 1, 30)

        # Time remaining to end the match
        time_remaining = (current_match_end_time - now).total_seconds() * 1000

        return schemas.HorseMatchTiming(is_horse_bidding_slot_open = True, remaining_time_in_millis = time_remaining)

    else:
        next_hour = now.hour + 1

        if next_hour == 24:
            next_hour = 0

        next_hour_time = datetime(now.year, now.month, now.day, next_hour, 0, 0)

        # Time remaining for next match
        time_difference = (next_hour_time - now).total_seconds() * 1000
        
        return schemas.HorseMatchTiming(is_horse_bidding_slot_open = False, remaining_time_in_millis = time_difference)
        

def is_bidding_allowed():
    time_slot = get_lottery_time_left_in_millis()

    if time_slot.is_horse_bidding_slot_open and time_slot.remaining_time_in_millis > 30000:
        return True
    else:
        return False


def calculate_winning_horse(db: Session):

    winning_horse = -1

    horse_min_bid_amount = 0

    for id in range(1,4):

        horse_bid_anount = db.query(func.sum(models.HorseRaceBids.bid_amount).label("bid_amount")).filter(models.HorseRaceBids.horse_id == id).first()

        if not horse_bid_anount or not horse_bid_anount.bid_amount:
            horse_bid_anount = 0
        else:
            horse_bid_anount = horse_bid_anount.bid_amount
        

        if id == 1:
            horse_min_bid_amount = horse_bid_anount
            winning_horse = id
        elif horse_bid_anount < horse_min_bid_amount:
                horse_min_bid_amount = horse_bid_anount
                winning_horse = id

    return winning_horse


def delete_prev_slot_entries(db: Session):
    now = datetime.now()

    db.query(models.HorseRaceBids).filter(models.HorseRaceBids.created_at < datetime(now.year, now.month, now.day, now.hour, 0, 0)).delete()

    db.commit()
   


