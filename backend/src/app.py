from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from clerk_backend_api import Clerk
from .routes import challenge, webhooks
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(challenge.router, prefix="/api/challenge")
app.include_router(webhooks.router, prefix="/api/webhooks")