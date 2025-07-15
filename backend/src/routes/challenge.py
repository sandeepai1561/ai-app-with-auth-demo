from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from ..ai_generator import generate_challenge_with_ai
from ..database.db import (
    get_challenge_quota,
    create_challenge_quota,
    create_challenge,
    get_user_challenges,
    reset_challenge_quota_if_needed,
)
from ..utils import authenticate_and_get_user_details
from ..database.models import get_db
from datetime import datetime
import json

router: APIRouter = APIRouter()

class ChallengeRequest(BaseModel):
    difficulty: str
    title: Optional[str] = None
    options: Optional[str] = None
    correct_answer_id: Optional[int] = None
    explanation: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "difficulty": "easy",
                "title": "What is the capital of France?",
                "options": "Paris, London, Berlin, Rome",
                "correct_answer_id": 1,
                "explanation": "The capital of France is Paris.",
            }
        }
@router.post("/generate-challenge")
async def generate_challenge(request: ChallengeRequest, db: Session = Depends(get_db)):
    """
    generate_challenge
    :param request:
    :param db:
    :return:
    """
    try:
        user_details = authenticate_and_get_user_details(request)
        user_id = user_details.get("user_id")

        quota = get_challenge_quota(db, user_id)
        if not quota:
            create_challenge_quota(db, user_id)

        quota = reset_challenge_quota_if_needed(db, quota)
        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Quota exceeded")

        # TODO: generate challenge
        challenge_data = generate_challenge_with_ai(request.difficulty)
        new_challenge = create_challenge(
            db=db,
            difficulty=request.difficulty,
            created_by=user_id,
            **challenge_data,
        )
        quota.quota_remaining -= 1
        db.commit()
        return {
            "id": new_challenge.id,
            "difficulty": new_challenge.difficulty,
            "title": new_challenge.title,
            "options": json.loads(new_challenge.options),
            "timestamp": new_challenge.data_created.isoformat(),
        }
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history(request: Request, db: Session = Depends(get_db)):
    """
    history
    :param request:
    :param db:
    :return:
    """
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")
    challenges = get_user_challenges(db, user_id)
    return {
        "challenges": challenges
    }

@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):
    """
    quota
    :param request:
    :param db:
    :return:
    """
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    quota = get_challenge_quota(db, user_id)
    if not quota:
        return {
            "user_id": user_id,
            "message": "Quota not found",
            "quota_remaining": 0,
            "last_reset_date": datetime.now()
        }
    quota = reset_challenge_quota_if_needed(db, quota)
    return quota