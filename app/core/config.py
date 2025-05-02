from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    ssl_key_path: str
    ssl_cert_path: str
    lm_folder: str
    templates_folder: str
    sqlalchemy_database_url: str

    class Config:
        env_file = ".env"

settings = Settings()