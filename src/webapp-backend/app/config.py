from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    TRIPLESTORE_ENDPOINT: str = Field("http://localhost:3030/testing/", env="TRIPLESTORE_ENDPOINT")
    INIT_ADMIN_MAIL: str = Field("admin@bfh.ch", env="INIT_ADMIN_MAIL")
    INIT_ADMIN_PW: str = Field("", env="INIT_ADMIN_PW")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MIN: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MIN")
    COMPILER_ENGINE_BASE_URL: str = Field("http://compiler-engine:8000", env="COMPILER_ENGINE_BASE_URL")
    TTN_APP_ID: str = Field("leaf-link-app", env="TTN_APP_ID") # TODO remove default value
    TTN_API_KEY: str = Field(..., env="TTN_API_KEY")

#    class Config:
#        env_file = ".env"  
#        env_file_encoding = "utf-8"

settings = Settings()
