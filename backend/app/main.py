from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {"message": "Blockchain Analytics API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}