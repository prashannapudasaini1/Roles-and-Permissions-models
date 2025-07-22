
from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    SECRET_KEY:str='supersecretkey'
    ALGORITHM:str='HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES:int=30
    DATABASE_URL: str = "postgresql://postgresql:Kanye%4012@localhost/auth_db"
    class Config:
        env_file='.env'
        
setting=Setting()