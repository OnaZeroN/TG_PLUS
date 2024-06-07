from enum import StrEnum
from abc import ABC, abstractmethod

from pyrogram.types import Message


class BaseCommand(ABC):
    @abstractmethod
    async def filter(self, message: Message) -> bool:
        """
        Filter for command
        :param message: Pyrogram message
        :return: Bool
        """

    async def execute(self, message: Message) -> None:
        """
        Execute command
        :param message: Pyrogram message
        """
        pass


class Commands(StrEnum):
    json: str = "!json"
    info: str = "!info"
    contact: str = "!contact"
    code: str = "!code"
