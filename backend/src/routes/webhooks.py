from fastapi import APIRouter, Request, HTTPException, Depends
from svix.webhooks import Webhook
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ..database.db import create_challenge_quota
from ..database.models import get_db
import os, json, logging

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
webhook_secret = os.getenv("WEBHOOK_SECRET")

router: APIRouter = APIRouter()

@router.post("/clerk")
async def handle_user_created(request: Request, db: Session = Depends(get_db)):
    """
    handle_user_created
    :param request:
    :param db:
    :return:
    """
    if not webhook_secret:
        return HTTPException(status_code=500, detail="WEBHOOK_SECRET not set")
    body = await request.body()
    payload = body.decode("utf-8")
    headers = dict(request.headers)
    try:
        wh = Webhook(webhook_secret)
        wh.verify(payload, headers)

        data = json.loads(payload)
        if data.get("type") != "user.created":
            return {
                "message": "Invalid webhook type",
                "status": "ignored"
            }
        user_data = data.get("data", {})
        user_id = user_data.get("id")
        create_challenge_quota(db, user_id)
        return {
            "message": "User created",
            "status": "success",
            "user_id": user_id,
            "code": 201
        }
    except Exception as e:
        return HTTPException(status_code=401, detail=str(e))