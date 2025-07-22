from pydantic import BaseSetting
class Setting(BaseSetting):
    SECRET_KEY:str='supersecretkey'
    ALGORITHM:str='HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES:int=30
    DATABASE_URL="postgresql://postgesql:Kanye@12@localhost/Users"
    class Config:
        env_file='.env'
setting=Setting()