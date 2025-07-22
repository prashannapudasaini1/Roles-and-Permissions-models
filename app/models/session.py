from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import Setting

engine = create_engine(Setting.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 