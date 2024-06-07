from __future__ import annotations

from app_config import AppConfig, CommonConfig, PostgresConfig


def create_app_config() -> AppConfig:
    return AppConfig(
        common=CommonConfig(),
        postgres=PostgresConfig()
    )
