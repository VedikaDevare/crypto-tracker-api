from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User, Watchlist
from schemas import WatchlistCreate, WatchlistResponse
from security import get_current_user

router = APIRouter()

@router.post("/watchlist", response_model=WatchlistResponse)
def add_to_watchlist(
    coin: WatchlistCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(
        User.username == current_user
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    supported_coins = ["bitcoin", "ethereum", "solana"]

    if coin.coin_id not in supported_coins:
        raise HTTPException(status_code=400, detail="Unsupported coin")

    existing_coin = db.query(Watchlist).filter(
        Watchlist.user_id == user.id,
        Watchlist.coin_id == coin.coin_id
    ).first()

    if existing_coin:
        raise HTTPException(status_code=409, detail="Coin already in watchlist")

    new_coin = Watchlist(
        user_id=user.id,
        coin_id=coin.coin_id
    )

    db.add(new_coin)
    db.commit()
    db.refresh(new_coin)

    return new_coin
@router.get("/watchlist", response_model=list[WatchlistResponse])
def check_watchlist(db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(
        User.username == current_user
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    watchlist = db.query(Watchlist).filter(
        Watchlist.user_id == user.id
    ).all()

    return watchlist
@router.delete("/watchlist/{coin_id}")
def remove_from_watchlist(
    coin_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(
        User.username == current_user
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    watchlist = db.query(Watchlist).filter(
        Watchlist.user_id == user.id,
        Watchlist.coin_id == coin_id
    ).first()

    if not watchlist:
        raise HTTPException(
            status_code=404,
            detail="Coin not found in your watchlist."
        )

    db.delete(watchlist)
    db.commit()

    return {"message": "Coin removed successfully"}
    