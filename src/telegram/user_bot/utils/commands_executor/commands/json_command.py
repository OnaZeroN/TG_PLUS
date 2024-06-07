import os

from pyrogram.types import Message

from .base_command import BaseCommand, Commands


class JsonCommand(BaseCommand):
    """
    Send json of telegram update
    """
    def __init__(self):
        self._trigger = Commands.json

    async def filter(self, message: Message) -> bool:
        return self._trigger in message.text and message.reply_to_message

    async def execute(self, message: Message) -> None:
        with open(f"data/temp/{message.reply_to_message.id}.json", "x") as file:
            file.write(message.__str__())
        await message.reply_document(
            reply_to_message_id=message.reply_to_message.id,
            caption=f'Json for update id: {message.reply_to_message.id}',
            document=f"data/temp/{message.reply_to_message.id}.json"
        )
        os.remove(f"data/temp/{message.reply_to_message.id}.json")
