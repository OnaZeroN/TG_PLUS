import asyncio

from app_config import AppConfig

from services.database.relational_db.base import Database
from services.database.relational_db.postgres import Postgres


def create_postgres(app_config: AppConfig) -> Database:
    db = Postgres(app_config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.create_tables())
    return db
