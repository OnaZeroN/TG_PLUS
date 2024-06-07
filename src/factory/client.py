from __future__ import annotations

from pyrogram import Client

from app_config import AppConfig
from services.database.relational_db.base import Database
from telegram.user_bot.handlers import get_userbot_handlers


def _include_di(client: Client, **kwargs) -> None:
    for key, value in kwargs.items():
        setattr(client, key, value)


def _register_handlers(client: Client) -> None:
    handlers = get_userbot_handlers()
    for handler in handlers:
        client.add_handler(handler)


def create_client(app_config: AppConfig, db: Database) -> Client:
    """
    :return: Configured ``Client`` with included handlers
    """
    client = Client(
        app_config.common.app_name,
        api_id=app_config.common.api_id,
        api_hash=app_config.common.api_hash.get_secret_value(),
        app_version=app_config.common.app_version,
        device_model=app_config.common.device_model,
        lang_pack=app_config.common.lang_pack,
        workdir=app_config.common.work_dir
    )
    _include_di(client=client, app_config=app_config, db=db)
    _register_handlers(client=client)
    return client
