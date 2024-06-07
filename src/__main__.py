from pyrogram import Client

from app_config import AppConfig
from services.database.relational_db.base import Database

from runners import run_client
from factory import create_app_config, create_client, create_postgres

from utils.loggers import setup_logger


def main() -> None:
    setup_logger()
    config: AppConfig = create_app_config()

    db: Database = create_postgres(app_config=config)
    client: Client = create_client(app_config=config, db=db)

    return run_client(client=client)


if __name__ == "__main__":
    main()
