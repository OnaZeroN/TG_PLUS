import os

from pyrogram import Client
from pyrogram.types import Message

from .base_command import BaseCommand, Commands


class InfoCommand(BaseCommand):
    """
    Send info about user/chat
    """

    def __init__(self, client: Client):
        self._client = client
        self._trigger = Commands.info

    async def filter(self, message: Message) -> bool:
        return self._trigger in message.text

    async def execute(self, message: Message) -> None:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            args = message.text.split(" ")
            if len(args) > 1:
                user_id = args[1]
                if user_id.strip().replace("-", "").isnumeric():
                    user_id = int(user_id)
            else:
                user_id = message.chat.id

        user_info = await self._client.get_chat(user_id)
        text = f"ℹ️User Info:\n\nUser Id: {user_info.id}\nUser DC: {user_info.dc_id}\n"
        await message.reply_text(
            reply_to_message_id=message.id,
            text=text
        )
