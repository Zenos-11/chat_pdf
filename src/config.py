from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str
    CHROMA_DB_PATH: str = "./chroma_db"
    EMBEDDING_MODEL_NAME: str = "moka-ai/m3e-base"
    model_config = SettingsConfigDict(env_file=".env") # Load environment variables from .env file
#单例模式
settings = Settings()