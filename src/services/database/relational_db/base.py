from __future__ import annotations

from typing import Optional
from abc import ABC, abstractmethod

from pydantic import BaseModel


class MessageInfo(BaseModel):
    message_id: int
    chat_id: int
    user: str
    text: Optional[str]
    file_path: Optional[str]

    @classmethod
    def build(cls, message_id: int, chat_id: int, user: str, text: str, file_path: Optional[str]) -> MessageInfo:
        """
        :param message_id: - telegram message id
        :param user: - telegram username or id
        :param chat_id: - telegram
        :param text: - telegram message text or caption
        :param file_path: - telegram message media file path
        """
        return cls(
            message_id=message_id,
            chat_id=chat_id,
            user=str(user),
            text=text,
            file_path=file_path
        )


class Database(ABC):

    @abstractmethod
    async def create_tables(self) -> None:
        """
        Create tables in database.
        """
        pass

    @abstractmethod
    async def add_message(self, message: MessageInfo) -> None:
        """
        Add message info to database
        :param message: MessageInfo
        :return: None
        """

    @abstractmethod
    async def get_message(self, message_id: int) -> MessageInfo | None:
        """
        Get message info from database
        :param message_id: telegram message id
        :return: MessageInfo object
        """
