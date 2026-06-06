from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings class using pydantic-settings to automatically
    load variables from a .env file or host environment variables.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Application Configuration
    app_name: str = "Library Management API"
    environment: str = "development"
    log_level: str = "INFO"
    
    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8000

# Singleton settings object
settings = Settings()
