import logging
import os
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType
from pyrogram.filters import private
from pyrogram.handlers import MessageHandler

from services.database.relational_db.base import Database, MessageInfo


async def on_message(client: Client, message: Message):
    if message.from_user.id == client.me.id:
        if not message.text:
            return
        if "!info" in message.text:
            args = message.text.split(" ")
            try:
                user_id = args[1]
            except IndexError:
                user_id = message.chat.id
            if user_id.strip().replace("-", "").isnumeric():
                user_id = int(user_id)
            user_info = await client.get_chat(user_id)
            text = f"ℹ️User Info:\n\nUser Id: {user_info.id}\nUser DC: {user_info.dc_id}\n"
            await message.reply_text(
                reply_to_message_id=message.id,
                text=text
            )
        elif "!json" in message.text:
            with open(f"data/temp/{message.reply_to_message.id}.json", "x") as file:
                file.write(message.__str__())
            await message.reply_document(
                reply_to_message_id=message.reply_to_message.id,
                caption=f'Json for update id: {message.reply_to_message.id}',
                document=f"data/temp/{message.reply_to_message.id}.json"
            )
            os.remove(f"data/temp/{message.reply_to_message.id}.json")
        elif "!file" in message.text:
            if message.reply_to_message.media:
                path = await client.download_media(message=message.reply_to_message, block=True)
                await message.reply_document(
                    document=path,
                    caption=f"файл из сообщения {message.reply_to_message.id}"
                )
        return

    await client.storage.save()

    db: Database = client.db
    app_config = client.app_config

    text = message.text or message.caption
    user = message.from_user.username or message.from_user.id

    logging.info(f"Message with id: {message.id} from: {user} saved!")
    path = None
    if message.media:
        path = await client.download_media(message=message, block=True)
        if message.media in [MessageMediaType.VOICE, MessageMediaType.PHOTO, MessageMediaType.VIDEO_NOTE, MessageMediaType.VIDEO]:
            media = getattr(message, str(message.media.value), None)
            if media.ttl_seconds:
                text = f"TTL Media from @{user}"
                await client.send_document(
                    chat_id=app_config.common.channel_id,
                    caption=text,
                    document=path
                )
    
    await db.add_message(
        MessageInfo.build(
            message_id=message.id,
            user=str(user),
            chat_id=message.chat.id,
            text=text,
            file_path=path
        )
    )


handler = MessageHandler(on_message, private)
