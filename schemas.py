from pydantic import BaseModel, EmailStr
from datetime import datetime

class CoinResponse(BaseModel):
    coin_id: str
    coin_name: str
    price_usd: float
    currency: str

class HistoryResponse(BaseModel):
    coin_id: str
    price_usd: float
    timestamp: datetime

class ChangeResponse(BaseModel):
    coin_id: str
    latest_price: float
    previous_price: float
    change: float
    percentage_change: float

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class WatchlistCreate(BaseModel):
    coin_id: str
class WatchlistResponse(BaseModel):
    id: int
    coin_id: str