from pydantic import BaseModel, SecretStr, Field
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict

from sqlalchemy import URL


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file="../.env.dist", env_file_encoding="utf-8")


class CommonConfig(BaseSettings, env_prefix="COMMON_"):
    api_id: int
    api_hash: SecretStr
    app_name: str = Field(default="TG_PLUS")
    app_version: str = Field(default="3.1.8 x64")
    device_model: str = Field(default="PC 64bit")
    lang_pack: str = Field(default="ru")
    work_dir: str = Field(default="data/session")

    channel_id: int


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    host: str
    name: str
    user: str
    port: int
    password: SecretStr

    def build_dsn(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


class AppConfig(BaseModel):
    common: CommonConfig
    postgres: PostgresConfig
