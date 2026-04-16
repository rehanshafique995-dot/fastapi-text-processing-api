import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Typed Text Processing API")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")


settings = Settings()