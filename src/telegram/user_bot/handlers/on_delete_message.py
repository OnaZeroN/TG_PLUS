import logging
from typing import List

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.handlers import DeletedMessagesHandler

from app_config import AppConfig
from services.database.relational_db.base import Database


async def on_delete_message(client: Client, messages: List[Message]) -> None:
    db: Database = client.db
    app_config: AppConfig = client.app_config

    for message in messages:
        message_info = await db.get_message(message.id)
        if not message_info:
            logging.warning(f"Message with id: {message.id} not found!")
            continue

        if not message_info.file_path:
            text = f"🗑 Message from @{message_info.user} was deleted:\n\n{message_info.text or ''}"
            await client.send_message(
                chat_id=app_config.common.channel_id,
                text=text
            )
        else:
            caption = f':\n\n{message_info.text}'
            text = f"🗑 Media from @{message_info.user} was deleted{caption if message_info.text else ''}"
            if not message_info.text:
                await client.send_message(
                    chat_id=app_config.common.channel_id,
                    text=text + ":"
                )
            await client.send_document(
                chat_id=app_config.common.channel_id,
                caption=text if message_info.text else None,
                document=message_info.file_path
            )

        logging.info(f"Message with id: {message.id} coped!")


handler = DeletedMessagesHandler(on_delete_message)
