from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    ssl_key_path: str
    ssl_cert_path: str
    audio_file_directory: str
    audio_file_name: str
    lm_directory: str
    templates_directory: str
    sqlalchemy_database_url: str
    client_base_url: str
    server_base_url: str

    class Config:
        env_file = ".env"

settings = Settings()