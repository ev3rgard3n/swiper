from fastapi import FastAPI

from src.config import DATABASE_URL
from src.auth.router import router as auth_router


app = FastAPI(title="Swiper")

app.include_router(auth_router)

@app.get("/")
def qwerr():
    ...