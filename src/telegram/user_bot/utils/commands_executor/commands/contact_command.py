from pyrogram import Client
from pyrogram.types import Message

from .base_command import BaseCommand, Commands


class ContactCommand(BaseCommand):
    """
    Send contact
    """

    def __init__(self, client: Client):
        self._client = client
        self._trigger = Commands.contact

    async def filter(self, message: Message) -> bool:
        return self._trigger in message.text

    async def execute(self, message: Message) -> None:
        args = message.text.split(" ")
        if len(args) > 1:
            phone_number = args[1]
        else:
            phone_number = "+888 0750 6369"

        await self._client.send_contact(
            chat_id=message.chat.id,
            phone_number=phone_number,
            first_name="GIT",
            last_name="TG PLUS"
        )
