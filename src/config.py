from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str
    CHROMA_DB_PATH: str = "./chroma_db"
    EMBEDDING_MODEL_NAME: str = "moka-ai/m3e-base"
    
    SECRET_KEY: str = "your-secret-key-keep-it-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file=".env")

#单例模式
settings = Settings()