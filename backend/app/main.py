from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import wallet
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blockchain Analytics API",
    description="API for blockchain transaction analysis and wallet tracking",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wallet.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Blockchain Analytics API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}