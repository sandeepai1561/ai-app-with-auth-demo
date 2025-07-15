from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models

def get_challenge_quota(db: Session, user_id: str):
    """
    get_challenge_quota
    :param db: Session
    :param user_id: str
    :return:
    """
    return (db.query(models.ChallengeQuota)
            .filter(models.ChallengeQuota.user_id == user_id)
            .first())

def create_challenge_quota(db: Session, user_id: str):
    """
    create_challenge_quota
    :param db: Session
    :param user_id: str
    :return:
    """
    db_challenge_quota = models.ChallengeQuota(
        user_id=user_id,
    )
    db.add(db_challenge_quota)
    db.commit()
    db.refresh(db_challenge_quota)
    return db_challenge_quota

def reset_challenge_quota_if_needed(db: Session, quota: models.ChallengeQuota):
    """
    reset_challenge_quota_if_needed
    :param db: Session
    :param quota: models.ChallengeQuota
    :return:
    """
    now = datetime.now()
    if quota.last_reset_date < now - timedelta(days=1):
        quota.quota_remaining = 50
        quota.last_reset_date = now
        db.commit()
        db.refresh(quota)
    return quota

def create_challenge(
        db: Session,
        difficulty: str,
        created_by: str,
        title: str,
        options: str,
        correct_answer_id: int,
        explanation: str,
):
    """
    create_challenge
    :param db:
    :param difficulty:
    :param created_by:
    :param title:
    :param options:
    :param correct_answer_id:
    :param explanation:
    :return:
    """
    db_challenge = models.Challenge(
        difficulty=difficulty,
        created_by=created_by,
        title=title,
        options=options,
        correct_answer_id=correct_answer_id,
        explanation=explanation
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def get_user_challenges(db: Session, user_id: str):
    """
    get_user_challenges
    :param db:
    :param user_id:
    :return:
    """
    return (db.query(models.Challenge)
            .filter(models.Challenge.user_id == user_id)
            .all())