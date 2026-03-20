from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "MediFlow AI"

    # Environment variables (NO hardcoding)
    DATABASE_URL: str
    OPENAI_API_KEY: str
    SMTP_USER: str
    SMTP_PASSWORD: str

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def async_database_url(self) -> str:
        return self.DATABASE_URL


settings = Settings()
