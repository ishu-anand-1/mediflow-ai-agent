from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MediFlow AI"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:Ishu9334277912@localhost:5432/internship"

    class Config:
        env_file = ".env"
        
    @property
    def async_database_url(self) -> str:
        # Directly returning the safe URL to prevent global system environment variable collisions
        return "postgresql+asyncpg://postgres:Ishu9334277912@localhost:5432/internship"

    @property
    def get_openai_api_key(self) -> str:
        return "Gn6cHfebcCimdBtC66Pl7vnrusCskj79"

    @property
    def smtp_user(self) -> str:
        return "talenthub.noreply@gmail.com"

    @property
    def smtp_password(self) -> str:
        return "edys qxlm urpn xuhs"

settings = Settings()
