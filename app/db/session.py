from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import setting

engine = create_engine(setting.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 