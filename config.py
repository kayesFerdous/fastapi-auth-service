from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 10
    ENV:str ="development"
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() #type: ignore
