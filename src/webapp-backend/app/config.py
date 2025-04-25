from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    TRIPLESTORE_ENDPOINT: str = Field("http://localhost:3030/testing/", env="TRIPLESTORE_ENDPOINT")
    INIT_ADMIN_MAIL: str = Field("admin@bfh.ch", env="INIT_ADMIN_MAIL")
    INIT_ADMIN_PW: str = Field("", env="INIT_ADMIN_PW")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MIN: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MIN")

#    class Config:
#        env_file = ".env"  
#        env_file_encoding = "utf-8"

settings = Settings()
