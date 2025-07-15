from sqlalchemy import Column, Integer, String, DateTime, create_engine, Engine, Any
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
DATABASE_URL = os.getenv("DATABASE_URL")

engine: Engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=20,
    max_overflow=0,
    pool_recycle=3600,
    # connect_args={"check_same_thread": False}
)
Base: Any = declarative_base()

class Challenge(Base):
    """
    Challenge
    """
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True)
    difficulty = Column(String(255), nullable=False)
    data_created = Column(DateTime, default=datetime.now)
    create_by = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    explanation = Column(String(255), nullable=False)
    options = Column(String(255), nullable=False)
    correct_answer_id = Column(Integer, nullable=False)

class User(Base):
    """
    User
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, unique=True)
    quota_remaining = Column(Integer, nullable=False, default=50)
    last_reset_date = Column(DateTime, nullable=False, default=datetime.now)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class ChallengeQuota(Base):
    """
    ChallengeQuota
    """
    __tablename__ = "challenge_quotas"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False)
    quota_remaining = Column(Integer, nullable=False, default=50)
    last_reset_date = Column(DateTime, nullable=False, default=datetime.now)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    get_db
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()