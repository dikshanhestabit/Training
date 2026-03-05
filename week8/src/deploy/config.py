import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuring model paths
    MODEL_PATH: str = os.getenv("MODEL_PATH", "src/quantized/model.gguf")
    MODEL_TYPE: str = "gguf"  # Options: gguf, int4 (transformers)
    
    # Configuring API settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Setting default generation parameters
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_TOP_P: float = 0.9
    DEFAULT_TOP_K: int = 40
    DEFAULT_MAX_TOKENS: int = 512
    DEFAULT_REPETITION_PENALTY: float = 1.1

    # Setting up logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
