from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_API_BASE: str = "https://api.deepseek.com/v1"
    OPENAI_MODEL_NAME: str = "deepseek-chat"
    REDIS_URL: str = "redis://localhost:6379"
    CHROMA_PATH: str = "./chroma_db"
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    WEBHOOK_SECRET: str = "your-webhook-secret-here"
    DINGTALK_WEBHOOK_URL: str = ""
    FEISHU_WEBHOOK_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
