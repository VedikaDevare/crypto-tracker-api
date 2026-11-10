import httpx
import os
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Price_history
from schemas import CoinResponse, HistoryResponse, ChangeResponse

router = APIRouter()
api_key = os.getenv("COINGECKO_API_KEY")

coin_names = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum",
    "solana": "Solana"
    }
supported_coins = ["bitcoin", "ethereum", "solana"]

@router.get("/coins/{coin_id}", response_model=CoinResponse)
def coin_data(coin_id: str, db: Session = Depends(get_db)):
    coin_name = coin_names.get(coin_id)
    if coin_id not in supported_coins:
        raise HTTPException(
           status_code=404,
           detail="Coin_id not found"
        )
    try:
        response = httpx.get(
            url=f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd",
            headers={"x-cg-demo-api-key": api_key},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        price = data[coin_id]["usd"]
        snapshot = Price_history(
            coin_id = coin_id,
            price_usd = price
        )
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)
        return {
            "coin_id": coin_id,
            "coin_name": coin_name,
            "price_usd": price,
            "currency": "USD",
            "timestamp": snapshot.timestamp
        }
    except httpx.HTTPStatusError as exc:
        print("CoinGecko Status:", exc.response.status_code)
        print("CoinGecko Error:", exc.response.text[:500])
        raise HTTPException(
            status_code=502,
            detail="Cryptocurrency provider returned an error"
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code= 502,
            detail = "Unable to connect to cryptocurrency provider"
        )
@router.get("/coins/{coin_id}/history", response_model=list[HistoryResponse])
def data_history(coin_id: str,limit: int = Query(default=5, ge=1, le=100),db: Session = Depends(get_db)):
    history = db.query(Price_history).filter(
        Price_history.coin_id == coin_id
    ).order_by(Price_history.timestamp.desc()).limit(limit).all()
    if not history:
        raise HTTPException(
            status_code=404,
            detail= f"No price history found for coin ID: {coin_id}"
        )
    return[
        {
            "coin_id": record.coin_id,
            "price_usd": record.price_usd,
            "timestamp": record.timestamp
        }
        for record in history
    ]
@router.get("/coins/{coin_id}/change", response_model=ChangeResponse)
def change_in_price(coin_id:str, db: Session = Depends(get_db)):
    data = db.query(Price_history).filter(
        Price_history.coin_id == coin_id
    ).order_by(Price_history.timestamp.desc()).limit(2).all()
    if len(data) < 2 :
        raise HTTPException(
            status_code=404,
            detail="Fewer than 2 snapshots found."
        )
    new_data = data[0]
    old_data = data[1]
    change = new_data.price_usd - old_data.price_usd
    if old_data.price_usd == 0:
        percentage_change = 0
    else:
        percentage_change = (change/old_data.price_usd)*100
    return{
        "coin_id": coin_id,
        "latest_price": new_data.price_usd,
        "previous_price": old_data.price_usd,
        "change": change,
        "percentage_change": percentage_change
    }


