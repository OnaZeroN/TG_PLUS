from typing import List
from pyrogram.handlers.handler import Handler


def get_userbot_handlers() -> List[Handler]:
    from . import on_delete_message, on_message

    return [
        on_delete_message.handler,
        on_message.handler
    ]
