from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Internal settings
    INIT_ADMIN_MAIL: str = Field("admin@bfh.ch", env="INIT_ADMIN_MAIL")
    INIT_ADMIN_PW: str = Field("", env="INIT_ADMIN_PW")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MIN: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MIN")
    
    # External services
    TRIPLESTORE_ENDPOINT: str = Field("http://fuseki:3030/testing/", env="TRIPLESTORE_ENDPOINT")
    COMPILER_ENGINE_BASE_URL: str = Field("http://compiler-engine:8000", env="COMPILER_ENGINE_BASE_URL")
    PROTOBUF_SERVICE_BASE_URL: str = Field("http://protobuf-service:8000", env="PROTOBUF_SERVICE_BASE_URL")
    
    # TTN settings
    FEATURE_TTN_ENABLED: bool = Field(True, env="FEATURE_TTN_ENABLED")
    TTN_APP_ID: str = Field("leaf-link-app", env="TTN_APP_ID")
    TTN_API_KEY: Optional[str] = Field(None, env="TTN_API_KEY")

#    class Config:
#        env_file = ".env"  
#        env_file_encoding = "utf-8"

settings = Settings()
