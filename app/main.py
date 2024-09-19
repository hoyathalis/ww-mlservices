# app/main.py

from fastapi import FastAPI
from app.api.api_v1.api import api_router

app = FastAPI(
    title="WalletWize Machine Learning Serivces",
    description="Serves all Machine Learning API's for Wallet Wize",
    version="1.0.0",)

app.include_router(api_router, prefix="/api/v1")
