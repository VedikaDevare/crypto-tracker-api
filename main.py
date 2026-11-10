from routes.coins import router as coins_router
from fastapi import FastAPI
from database import Base, engine
from models import User, Price_history, Watchlist
from routes.users import router as users_router
from routes.watchlist import router as watchlist_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

(Base.metadata.create_all(bind=engine))

app.include_router(coins_router)
app.include_router(users_router)
app.include_router(watchlist_router)

    
@app.get("/")
def check():
    return {"message": "Crypto Tracker API is running"}
